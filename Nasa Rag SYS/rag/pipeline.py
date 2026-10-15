from .ml.predict import predict as predict_fire
# ============================================================
# RAG PIPELINE ORCHESTRATOR
# ============================================================


import re



def enforce_prediction_schema(response, ml_prediction, question):
    """Keep real ML outputs separate from experimental measurements."""

    if not isinstance(response, dict):
        return response

    # Never trust a prediction invented by the LLM.
    response["prediction"] = None

    if ml_prediction is None:
        return response

    records = (
        [ml_prediction]
        if isinstance(ml_prediction, dict)
        else ml_prediction
    )

    if not isinstance(records, list):
        return response

    match = re.search(r"\bEXP-\d+\b", question, re.IGNORECASE)
    requested_id = match.group(0).upper() if match else None

    valid_predictions = []

    for record in records:
        if not isinstance(record, dict):
            continue

        experiment_id = record.get("experiment_id")

        # Exact experiment questions must match that experiment.
        if requested_id and str(experiment_id).upper() != requested_id:
            continue

        actual = record.get("prediction")

        # Support a direct model output as well.
        if not isinstance(actual, dict):
            if "label" in record and "probability" in record:
                actual = record
            else:
                continue

        if "label" not in actual or "probability" not in actual:
            continue

        valid_predictions.append({
            "experiment_id": experiment_id,
            **actual,
        })

    if not valid_predictions:
        response["prediction"] = None

    elif requested_id:
        # One matching prediction for an exact experiment question.
        response["prediction"] = valid_predictions[0]

    else:
        # Preserve predictions for broad questions, without
        # arbitrarily selecting one experiment.
        response["prediction"] = valid_predictions

    return response


class RAGPipeline:

    def __init__(
        self,
        retriever,
        reranker,
        metadata_filter,
        context_selector,
        context_builder,
        answerability_gate,
        response_generator,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.metadata_filter = metadata_filter
        self.context_selector = context_selector
        self.context_builder = context_builder
        self.answerability_gate = answerability_gate
        self.response_generator = response_generator

    def _experiment_id(self, candidate):
        metadata = candidate.get("metadata", {})

        value = metadata.get("experiment_id")
        if value:
            return str(value).upper()

        text = str(candidate.get("text", ""))
        match = re.search(r"\bEXP[-_ ]?\d+\b", text.upper())

        return match.group(0).replace("_", "-") if match else None


    def _field_value(self, text, aliases):
        clean_text = str(text).lower()

        # Normalize Markdown formatting and line breaks.
        clean_text = re.sub(r"[*_`]", "", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text)

        for alias in aliases:
            pattern = (
                r"\b"
                + re.escape(alias)
                + r"\b\s*"
                + r"(?:(?:was|is|of|:)\s*)*"
                + r"([-+]?\d+(?:\.\d+)?)"
                + r"\s*"
                + r"([a-zA-Z%/³^.-]*)"
              )

            match = re.search(pattern, clean_text)

            if match:
                value = float(match.group(1))
                unit = match.group(2).strip()
                return value, unit

        return None, None


    def _knowledge_base_response(self, question, candidates):
        q = question.lower()
        requested_id = self._experiment_id({
             "text": question,
             "metadata": {}
                    })
        requested_fields = {
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

        requested_field = next(
            (
                field for field in sorted(
                    requested_fields, key=len, reverse=True
                )
                if field in q
            ),
            None,
        )

        evidence = []
        sources = []
        answer_parts = []

        for candidate in candidates:
            text = str(candidate.get("text", ""))
            metadata = candidate.get("metadata", {})
            experiment_id = self._experiment_id(candidate)

            if requested_id and experiment_id != requested_id:
                    continue

            # Preserve evidence only when the requested field
            # and its numeric value are actually present.
            if requested_field:
                value, unit = self._field_value(
                    text, requested_fields[requested_field]
                )

                if value is None:
                    continue

                finding = (
                    f"Observed {requested_field}: {value:g}"
                    f"{(' ' + unit) if unit else ''}."
                )

                item = {
                    "experiment_id": experiment_id,
                    "measurement": requested_field,
                    "value": value,
                    "unit": unit,
                    "finding": finding,
                }

                evidence.append(item)
                answer_parts.append(
                    f"{experiment_id}: {finding}"
                )

                if experiment_id not in sources:
                    sources.append(experiment_id)

            else:
                # Don't invent an answer to a broad question
                # using a generic chunk summary.
                continue

        if not evidence:
            return None

        return {
            "answer": " ".join(answer_parts),
            "experimental_evidence": evidence,
            "prediction": None,
            "observed_trends": [],
            "interpretation": (
                "Values are reported experimental observations, "
                "not machine-learning predictions."
            ),
            "safety_insight": (
                "Interpret the measurement within the specific "
                "experimental conditions; do not generalize it "
                "to other conditions without supporting evidence."
            ),
            "limitations": [
                "This response reports retrieved measurements only.",
                "No prediction was generated."
            ],
            "sources": sources,
            "source": "knowledge_base",
        }


    def _predict_from_retrieved_experiments(self, results):
        """Predict fire risk using conditions from retrieved experiments."""
        from ml.predict import predict as predict_fire

        predictions = []
        seen_experiments = set()

        required_fields = [
            "oxygen_concentration_pct",
            "pressure_kpa",
            "flow_velocity_cm_s",
            "ambient_temperature_c",
            "material",
            "flow_configuration",
        ]

        for item in results:
            # Support metadata stored in different result structures
            metadata = item.get("metadata", {})

            if not metadata and isinstance(item.get("document"), dict):
                metadata = item["document"].get("metadata", {})

            if not metadata:
                metadata = item

            experiment_id = metadata.get("experiment_id")

            # Avoid predicting repeatedly for multiple chunks of one experiment
            if not experiment_id or experiment_id in seen_experiments:
                continue

            seen_experiments.add(experiment_id)

            # Never silently use model defaults for missing experiment data
            missing = [
                field for field in required_fields
                if metadata.get(field) is None
                or metadata.get(field) == ""
            ]

            if missing:
                predictions.append({
                    "experiment_id": experiment_id,
                    "status": "insufficient_input",
                    "missing_fields": missing,
                })
                continue

            conditions = {
                field: metadata[field]
                for field in required_fields
            }

            try:
                prediction = predict_fire(conditions)

                predictions.append({
                    "experiment_id": experiment_id,
                    "status": "predicted",
                    "conditions": conditions,
                    "prediction": prediction,
                })

            except (ValueError, TypeError) as exc:
                predictions.append({
                    "experiment_id": experiment_id,
                    "status": "prediction_error",
                    "reason": str(exc),
                })

        return predictions or None

    
    def answer(self, question, conditions=None, ml_prediction=None):
        # 1. Hybrid retrieval
        hybrid_results = self.retriever.search(
            query=question,
            dense_top_k=20,
            bm25_top_k=20,
            top_k=20,
        )

        # 2. Enrich retrieved chunks with metadata
        enriched_results = self.metadata_filter.enrich_results(
            hybrid_results
        )

        # 3. Cross-encoder reranking
        reranked_results = self.reranker.rerank(
            query=question,
            candidates=enriched_results,
            top_k=2,
        )

        # 4. Check whether the evidence can answer the question
        gate_result = self.answerability_gate.check(
            question,
            reranked_results,
        )
        
        if ml_prediction is None:
            ml_prediction = self._predict_from_retrieved_experiments(
            reranked_results
        )
        
        # 5. Select evidence and build the LLM context
        selected_results = self.context_selector.select(
            reranked_results
        )

            
        context = self.context_builder.build(
            selected_results
        )

        
        print("DEBUG question:", question)
        print("DEBUG context type:", type(context))
        print("DEBUG ml_prediction:", repr(ml_prediction))
        print("DEBUG response_generator:", type(self.response_generator))
        
        # 6. Generate the LLM response first
        response = self.response_generator.generate(
            question=question,
            context=context,
            ml_prediction=ml_prediction,
        )

        # 7. Enforce the prediction schema
        response = enforce_prediction_schema(
            response=response,
            ml_prediction=ml_prediction,
            question=question,
        )
        # 7. Return the complete result
        return {
            "response": response,
            "answerability": gate_result,
            "retrieved_results": reranked_results,
        }
