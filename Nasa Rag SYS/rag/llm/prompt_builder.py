# ============================================================
# PROMPT BUILDER
# ============================================================
import json

class PromptBuilder:

    def __init__(self):
        pass


    def build(
        self,
        question,
        context,
        ml_prediction=None
    ):
        """
        Build the structured scientific response prompt.
        """

        # ====================================================
        # ML INFORMATION
        # ====================================================
        if ml_prediction is None:
            ml_section = """
No machine learning prediction is available.

Therefore:
- prediction must be null
- do not invent a prediction
- do not estimate numerical values
""".strip()

        else:
            ml_section = f"""
A machine learning model produced the following prediction data:

{json.dumps(ml_prediction, indent=2, ensure_ascii=False, default=str)}

Rules:
- Treat these values as MODEL PREDICTIONS, not experimental measurements.
- Preserve experiment IDs, predicted labels, probabilities,
  risk bands, and model names when available.
- Do not invent or modify prediction values.
- If an experiment has missing required inputs, report that no
  prediction was generated for that experiment.
- The model was trained on simulated data and is not certified
  fire-safety guidance.
- The prediction field must contain only the ML model's prediction.
- Preserve the actual model label, probability, risk band, and model name.
- Never place observed flame-spread rates or oxygen measurements in prediction.
- If no ML prediction exists, return null.
- Experimental measurements belong in experimental_evidence.
- Do not invent a prediction to fill the field.
""".strip()



        # ====================================================
        # FINAL PROMPT
        # ====================================================

        prompt = f"""
You are the scientific reasoning component of the
"Flame in Freefall" microgravity combustion system.

The system retrieved scientific evidence from its knowledge
base.

Your job is to produce a structured scientific response.

============================================================
USER QUESTION
============================================================

{question}

============================================================
RETRIEVED EXPERIMENTAL EVIDENCE
============================================================

{context}

============================================================
MACHINE LEARNING INFORMATION
============================================================

{ml_section}

============================================================
IMPORTANT SCIENTIFIC RULES
============================================================

1. Use the retrieved evidence as the primary source.

2. NEVER invent experiment IDs.

3. NEVER invent experimental measurements.

4. NEVER invent oxygen concentrations, temperatures,
   pressures, flow velocities, risk scores, or other values.

5. If a value is not present in the evidence, use null
   where the schema permits it.

6. Clearly distinguish experimental observations from
   machine-learning predictions.

7. A machine-learning prediction is NOT an experimental
   measurement.

8. Do not claim that one variable caused another unless
   the evidence supports a causal relationship.

9. When comparing experiments, remember that multiple
   experimental conditions may differ simultaneously.

10. If the evidence only shows an association, describe it
    as an association rather than proven causation.

11. Use experiment IDs in the experimental_evidence field.

12. The sources field should contain the experiment IDs
    that support the response.

13. If no ML prediction is available, prediction MUST be null.

14. observed_trends must describe trends supported by the
    retrieved evidence.

15. interpretation should explain what the evidence means,
    without introducing unsupported facts.

16. safety_insight should only contain safety conclusions
    supported by the evidence.

17. limitations should mention important uncertainties,
    missing variables, or limitations of the evidence.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

The JSON must contain exactly these top-level fields:

{{
    "answer": "...",
    "experimental_evidence": [],
    "prediction": null,
    "observed_trends": [],
    "interpretation": "...",
    "safety_insight": "...",
    "limitations": [],
    "sources": []
}}

============================================================
FIELD DEFINITIONS
============================================================

answer:
A concise direct answer to the user's question.

experimental_evidence:
The experiments from the retrieved evidence that support
the answer.

Each item should contain:

- experiment_id
- oxygen_concentration
- flame_temperature
- source
- finding

Use null when a numerical field is not available.


ML PREDICTION RULES:
- Use the supplied predictions generated from retrieved experiment conditions.
- Preserve each experiment ID, predicted label, probability, and risk band.
- Distinguish predicted fire outcomes from observed experimental outcomes.
- Never claim a prediction is an actual experimental measurement.
- If inputs are missing, explain that a prediction could not be generated
  for that experiment.
- If ml_prediction is null, return prediction as null.
- State that the model was trained on simulated data and is not certified
  fire-safety guidance.


observed_trends:
Always return a non-empty list containing at least one descriptive item.

Each item should contain:
- trend
- evidence_status
- explanation
- experiment_ids

Rules:
- Use "supported" when the retrieved experimental evidence
  establishes the trend.
- Use "insufficient_evidence" when the available experiments
  do not establish a relationship.
- Use "general_scientific_context" only for general scientific
  information, clearly distinguished from experimental findings.
- If a relationship cannot be established, describe what the
  retrieved experiments actually show and explain what evidence
  is missing.
- Never invent measurements, experiment IDs, or relationships.
- Do not label a trend as observed unless it is supported
  by experimental observations.


interpretation:
Always provide a meaningful scientific interpretation of the
available evidence. Explain what can be concluded and what
remains uncertain. Distinguish experimental findings from
general scientific reasoning.

safety_insight:
Relevant fire-safety implication supported by the evidence.

limitations:
Always return a non-empty list of specific limitations.
Identify missing measurements, insufficient evidence, uncertainty,
or the absence of an ML prediction when relevant.

sources:
Experiment IDs used to support the response.

============================================================
FINAL RESPONSE
============================================================
""".strip()

        return prompt