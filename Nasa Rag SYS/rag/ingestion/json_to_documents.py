import json
from pathlib import Path


# =========================
# Configuration
# =========================

INPUT_FILE = Path(r"C:\Users\User\Nasa Rag SYS\Data\raw\Experiments.json")
OUTPUT_DIR = Path(r"C:\Users\User\Nasa Rag SYS\knowledge_base\experiments")


# =========================
# Create output directory
# =========================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# Load JSON
# =========================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    experiments = json.load(f)


# =========================
# Convert one experiment
# =========================

def experiment_to_markdown(exp):
    return f"""---
experiment_id: {exp["experiment_id"]}
source_investigation: {exp["source_investigation"]}
material: {exp["material"]}
material_type: {exp["material_type"]}
flow_configuration: {exp["flow_configuration"]}
oxygen_concentration_pct: {exp["oxygen_concentration_pct"]}
pressure_kpa: {exp["pressure_kpa"]}
flow_velocity_cm_s: {exp["flow_velocity_cm_s"]}
ambient_temperature_c: {exp["ambient_temperature_c"]}
outcome: {exp["outcome"]}
risk_level: {exp["risk_level"]}
test_date: {exp["test_date"]}
---

# Experiment {exp["experiment_id"]}

## Investigation

- **Source Investigation:** {exp["source_investigation"]}

## Material

- **Material:** {exp["material"]}
- **Material Type:** {exp["material_type"]}

## Experimental Conditions

- **Flow Configuration:** {exp["flow_configuration"]}
- **Oxygen Concentration:** {exp["oxygen_concentration_pct"]} %
- **Pressure:** {exp["pressure_kpa"]} kPa
- **Flow Velocity:** {exp["flow_velocity_cm_s"]} cm/s
- **Ambient Temperature:** {exp["ambient_temperature_c"]} °C

## Observed Results

- **Ignition Time:** {exp["ignition_time_s"]} s
- **Flame Spread Rate:** {exp["flame_spread_rate_mm_s"]} mm/s
- **Heat Release Rate:** {exp["heat_release_rate_kw"]} kW
- **Soot Volume Fraction:** {exp["soot_volume_fraction_ppm"]} ppm
- **Outcome:** {exp["outcome"]}

## Fire Risk

- **Risk Score:** {exp["risk_score"]}
- **Risk Level:** {exp["risk_level"]}

## Experimental Summary

Experiment {exp["experiment_id"]} was conducted as part of the
{exp["source_investigation"]} investigation using {exp["material"]}.

The experiment used an oxygen concentration of
{exp["oxygen_concentration_pct"]}%, a pressure of
{exp["pressure_kpa"]} kPa, and a flow velocity of
{exp["flow_velocity_cm_s"]} cm/s.

The observed flame spread rate was
{exp["flame_spread_rate_mm_s"]} mm/s, with a heat release rate of
{exp["heat_release_rate_kw"]} kW.

The observed outcome was **{exp["outcome"]}**, with a calculated
risk score of {exp["risk_score"]} and a **{exp["risk_level"]}**
risk level.
"""


# =========================
# Generate Markdown files
# =========================

created = 0

for experiment in experiments:

    experiment_id = experiment["experiment_id"]

    output_file = OUTPUT_DIR / f"{experiment_id}.md"

    markdown = experiment_to_markdown(experiment)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    created += 1


# =========================
# Summary
# =========================

print(f"Successfully created {created} Markdown documents.")
print(f"Output directory: {OUTPUT_DIR}")