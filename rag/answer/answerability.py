
# ============================================================
# ANSWERABILITY GATE
# ============================================================

import re


class AnswerabilityGate:

    def __init__(
        self,
        min_reranker_score=-4.0,
        min_query_coverage=0.20,
        min_candidates=1,
    ):
        self.min_reranker_score = min_reranker_score
        self.min_query_coverage = min_query_coverage
        self.min_candidates = min_candidates

        self.stopwords = {
            "a", "an", "the", "is", "are", "was", "were",
            "do", "does", "did", "how", "what", "when",
            "where", "why", "which", "who", "in", "on",
            "at", "of", "to", "for", "and", "or", "with",
            "by", "from", "about", "between", "into",
            "affect", "effects", "effect", "happens",
            "happen", "show", "shows", "using", "used",
        }

        self.field_aliases = {
            "flame spread rate": [
                "flame spread rate", "spread rate"
            ],
            "heat release rate": ["heat release rate"],
            "ignition time": ["ignition time"],
            "soot volume fraction": ["soot volume fraction"],
            "oxygen concentration": ["oxygen concentration"],
            "pressure": ["pressure"],
            "flow velocity": ["flow velocity"],
            "risk score": ["risk score"],
            "risk level": ["risk level"],
        }

    def _tokens(self, text):
        words = re.findall(r"[a-zA-Z0-9]+", str(text).lower())
        return {
            word for word in words
            if word not in self.stopwords and len(word) > 1
        }

    def _query_coverage(self, question, candidates):
        query_tokens = self._tokens(question)

        if not query_tokens:
            return 0.0

        evidence_text = " ".join(
            str(c.get("text", "")) + " " +
            str(c.get("metadata", {}))
            for c in candidates
        )

        evidence_tokens = self._tokens(evidence_text)
        matched = query_tokens.intersection(evidence_tokens)

        return len(matched) / len(query_tokens)

    def _requested_experiment_id(self, question):
        match = re.search(
            r"\bEXP[-_ ]?\d+\b",
            question.upper()
        )

        if not match:
            return None

        return re.sub(
            r"[-_ ]",
            "-",
            match.group(0)
        )

    def _normalize_experiment_id(self, value):
        match = re.search(
            r"\bEXP[-_ ]?\d+\b",
            str(value).upper()
        )

        if not match:
            return None

        return re.sub(
            r"[-_ ]",
            "-",
            match.group(0)
        )

    def _requested_field(self, question):
        q = question.lower()

        # Match the longest field names first.
        for field in sorted(
            self.field_aliases,
            key=len,
            reverse=True
        ):
            if field in q:
                return field

        return None

    def _has_numeric_field(self, text, field):
        # Remove Markdown emphasis so **Field:** is handled.
        clean_text = re.sub(r"[*_`]", "", str(text).lower())

        for alias in self.field_aliases[field]:
            pattern = (
                re.escape(alias)
                + r"\s*"
                + r"(?:(?:is|was|of)\s+)?"
                + r":?\s*"
                + r"[-+]?\d+(?:\.\d+)?"
            )

            if re.search(pattern, clean_text):
                return True

        return False

    def _validate_exact_evidence(self, question, candidates):
        experiment_id = self._requested_experiment_id(question)

        # Exact-field validation applies to explicit experiment
        # questions. General questions use relevance checks below.
        if experiment_id is None:
            return True, "No explicit experiment ID to validate."

        field = self._requested_field(question)

        if field is None:
            return (
                False,
                "The requested measurement is not supported "
                "by the configured field validator."
            )

        matching_experiments = []

        for candidate in candidates:
            metadata = candidate.get("metadata", {})
            text = str(candidate.get("text", ""))

            metadata_id = self._normalize_experiment_id(
                metadata.get("experiment_id", "")
            )

            text_ids = {
                self._normalize_experiment_id(match)
                for match in re.findall(
                    r"\bEXP[-_ ]?\d+\b",
                    text.upper()
                )
            }

            if (
                metadata_id == experiment_id
                or experiment_id in text_ids
            ):
                matching_experiments.append(candidate)

        if not matching_experiments:
            return (
                False,
                f"Experiment {experiment_id} was not found "
                "in retrieved evidence."
            )

        for candidate in matching_experiments:
            if self._has_numeric_field(
                candidate.get("text", ""),
                field
            ):
                return (
                    True,
                    f"Experiment {experiment_id} contains "
                    f"a numeric value for {field}."
                )

        return (
            False,
            f"Experiment {experiment_id} was retrieved, "
            f"but a numeric value for {field} was not found."
        )

    def check(self, question, candidates):
        candidates = candidates or []

        usable = [
            c for c in candidates
            if str(c.get("text", "")).strip()
        ]

        coverage = self._query_coverage(question, usable)

        if len(usable) < self.min_candidates:
            return {
                "answerable": False,
                "decision": "llm_fallback",
                "reason": "No usable retrieved evidence.",
                "top_score": None,
                "query_coverage": coverage,
                "candidate_count": len(usable),
            }

        scores = [
            float(c["reranker_score"])
            for c in usable
            if c.get("reranker_score") is not None
        ]

        if not scores:
            return {
                "answerable": False,
                "decision": "llm_fallback",
                "reason": "Reranker scores are missing.",
                "top_score": None,
                "query_coverage": coverage,
                "candidate_count": len(usable),
            }

        top_score = max(scores)

        if top_score < self.min_reranker_score:
            return {
                "answerable": False,
                "decision": "llm_fallback",
                "reason": "Reranker score is below threshold.",
                "top_score": top_score,
                "query_coverage": coverage,
                "candidate_count": len(usable),
            }

        if coverage < self.min_query_coverage:
            return {
                "answerable": False,
                "decision": "llm_fallback",
                "reason": "Insufficient query-term coverage.",
                "top_score": top_score,
                "query_coverage": coverage,
                "candidate_count": len(usable),
            }

        evidence_ok, evidence_reason = (
            self._validate_exact_evidence(question, usable)
        )

        if not evidence_ok:
            return {
                "answerable": False,
                "decision": "llm_fallback",
                "reason": evidence_reason,
                "top_score": top_score,
                "query_coverage": coverage,
                "candidate_count": len(usable),
            }

        return {
            "answerable": True,
            "decision": "knowledge_base",
            "reason": evidence_reason,
            "top_score": top_score,
            "query_coverage": coverage,
            "candidate_count": len(usable),
        }
