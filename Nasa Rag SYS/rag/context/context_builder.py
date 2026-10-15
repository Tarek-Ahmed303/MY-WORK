# ============================================================
# CONTEXT BUILDER
# ============================================================

class ContextBuilder:

    def __init__(self):
        pass

    def build(self, selected_results):
        """
        Build an LLM-ready context from selected
        retrieval results.

        Parameters
        ----------
        selected_results : list
            Results selected by ContextSelector.

        Returns
        -------
        str
            Formatted context.
        """

        if not selected_results:
            return (
                "No relevant experimental evidence "
                "was retrieved."
            )

        context_parts = []

        # ----------------------------------------------------
        # Build each evidence block
        # ----------------------------------------------------

        for result in selected_results:

            metadata = result.get(
                "metadata",
                {}
            )

            experiment_id = metadata.get(
                "experiment_id",
                "Unknown"
            )

            investigation = metadata.get(
                "source_investigation",
                "Unknown"
            )

            material = metadata.get(
                "material",
                "Unknown"
            )

            material_type = metadata.get(
                "material_type",
                "Unknown"
            )

            oxygen = metadata.get(
                "oxygen_concentration_pct",
                "Unknown"
            )

            pressure = metadata.get(
                "pressure_kpa",
                "Unknown"
            )

            flow_velocity = metadata.get(
                "flow_velocity_cm_s",
                "Unknown"
            )

            temperature = metadata.get(
                "ambient_temperature_c",
                "Unknown"
            )

            outcome = metadata.get(
                "outcome",
                "Unknown"
            )

            risk_level = metadata.get(
                "risk_level",
                "Unknown"
            )

            text = result.get(
                "text",
                ""
            ).strip()

            context_rank = result.get(
                "context_rank",
                "Unknown"
            )

            # ------------------------------------------------
            # Evidence block
            # ------------------------------------------------

            evidence = f"""
[EVIDENCE {context_rank}]

Experiment ID: {experiment_id}
Investigation: {investigation}
Material: {material}
Material Type: {material_type}

Experimental Conditions:
- Oxygen concentration: {oxygen}%
- Pressure: {pressure} kPa
- Flow velocity: {flow_velocity} cm/s
- Ambient temperature: {temperature} °C

Outcome: {outcome}
Risk level: {risk_level}

Experimental Evidence:
{text}
""".strip()

            context_parts.append(
                evidence
            )

        # ----------------------------------------------------
        # Combine evidence
        # ----------------------------------------------------

        context = "\n\n".join(
            context_parts
        )

        return context