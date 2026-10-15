"""Shared feature + target definitions for the fire-prediction model.

Keeping this in one place guarantees train.py and predict.py agree on exactly
which columns feed the model and how the label is defined — so the saved
artifact and the inference code can never drift apart.
"""
from __future__ import annotations

# Pre-test cabin conditions only. We deliberately EXCLUDE anything measured
# during/after the burn (ignition_time_s, flame_spread_rate_mm_s,
# heat_release_rate_kw, soot_volume_fraction_ppm) and the derived labels
# (risk_score, risk_level, outcome) — using them would leak the answer.
NUMERIC_FEATURES = [
    "oxygen_concentration_pct",
    "pressure_kpa",
    "flow_velocity_cm_s",
    "ambient_temperature_c",
]
CATEGORICAL_FEATURES = [
    "material",
    "material_type",
    "flow_configuration",
]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Target: a SUSTAINED fire. steady_spread + flash_fire -> 1 (fire),
# extinguished + self_extinguished -> 0 (no sustained fire).
FIRE_OUTCOMES = {"steady_spread", "flash_fire"}
TARGET = "fire"

# Accepted input aliases so callers using mobile-style keys still work.
ALIASES = {
    "o2": "oxygen_concentration_pct",
    "o2_pct": "oxygen_concentration_pct",
    "oxygen": "oxygen_concentration_pct",
    "pressure": "pressure_kpa",
    "pressure_kpa": "pressure_kpa",
    "flow": "flow_velocity_cm_s",
    "flow_cm_s": "flow_velocity_cm_s",
    "flow_velocity": "flow_velocity_cm_s",
    "temperature": "ambient_temperature_c",
    "ambient_temperature": "ambient_temperature_c",
    "temp": "ambient_temperature_c",
    "flow_configuration": "flow_configuration",
    "flow_config": "flow_configuration",
    "material_type": "material_type",
    "material": "material",
}

DEFAULTS = {
    "oxygen_concentration_pct": 20.9,
    "pressure_kpa": 101.3,
    "flow_velocity_cm_s": 14.0,
    "ambient_temperature_c": 22.5,
    "material": "PMMA (acrylic)",
    "material_type": "solid",
    "flow_configuration": "concurrent",
}

# material -> material_type lookup, so callers can omit material_type.
MATERIAL_TYPE = {
    "PMMA (acrylic)": "solid",
    "Teflon": "solid",
    "Silicone rubber": "solid",
    "Nomex": "solid",
    "Cotton-fiberglass fabric": "solid",
    "Heptane droplet": "liquid_droplet",
    "Methanol droplet": "liquid_droplet",
}


def label_fire(outcome: str) -> int:
    return 1 if outcome in FIRE_OUTCOMES else 0


def normalize_input(raw: dict) -> dict:
    """Map aliases, infer material_type, and fill defaults. Returns a dict with
    exactly the FEATURES keys, ready for the model. Raises ValueError on bad
    numeric values."""
    row: dict = {}
    for k, v in (raw or {}).items():
        key = ALIASES.get(k, k)
        if key in FEATURES:
            row[key] = v
    if "material" in row and "material_type" not in row:
        mt = MATERIAL_TYPE.get(row["material"])
        if mt:
            row["material_type"] = mt
    for f in FEATURES:
        if row.get(f) in (None, ""):
            row[f] = DEFAULTS[f]
    for f in NUMERIC_FEATURES:
        try:
            row[f] = float(row[f])
        except (TypeError, ValueError):
            raise ValueError(f"{f} must be numeric, got {row[f]!r}")
    for f in CATEGORICAL_FEATURES:
        row[f] = str(row[f])
    return {f: row[f] for f in FEATURES}
