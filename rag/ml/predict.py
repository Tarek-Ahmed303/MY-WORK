"""Load the trained fire-prediction model and score cabin conditions.

Standalone — the only dependency is the saved artifact
(ml/artifacts/fire_model.joblib). Import `predict` from your code, or run the
CLI. The model and its feature contract are loaded once and cached.

    from ml.predict import predict
    predict({"material": "PMMA (acrylic)", "oxygen_concentration_pct": 19.0,
             "pressure_kpa": 101.3, "flow_velocity_cm_s": 6.0,
             "ambient_temperature_c": 24})
    # -> {"fire": True, "probability": 0.87, "label": "fire",
    #     "riskBand": "HIGH", "threshold": 0.5, "inputs": {...}}

CLI:
    python ml/predict.py --material "PMMA (acrylic)" --o2 19 --flow 6 --pressure 101.3 --temp 24
    python ml/predict.py --json '{"material":"Nomex","o2":14}'
"""
from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import joblib

from ml.features import FEATURES, normalize_input

MODEL_PATH = ROOT / "ml" / "artifacts" / "fire_model.joblib"


class ModelNotTrained(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load() -> dict:
    if not MODEL_PATH.exists():
        raise ModelNotTrained(
            f"{MODEL_PATH.relative_to(ROOT)} not found — run `python ml/train.py` first.")
    return joblib.load(MODEL_PATH)


def model_info() -> dict:
    bundle = _load()
    return {
        "model_name": bundle["model_name"],
        "features": bundle["features"],
        "target": bundle["target"],
        "fire_outcomes": bundle["fire_outcomes"],
        "threshold": bundle["threshold"],
        "sklearn_version": bundle["sklearn_version"],
    }


def _band(p: float) -> str:
    return "HIGH" if p >= 0.66 else "MED" if p >= 0.33 else "LOW"


def predict(conditions: dict) -> dict:
    """Predict sustained-fire probability for one set of cabin conditions.

    Accepts dataset keys or aliases (o2, flow, pressure, temp, material,
    flow_configuration); missing fields fall back to cabin-nominal defaults and
    material_type is inferred from material. Returns a JSON-serializable dict."""
    bundle = _load()
    row = normalize_input(conditions)
    x = np.array([[row[f] for f in FEATURES]], dtype=object)
    proba = float(bundle["pipeline"].predict_proba(x)[0, 1])
    threshold = bundle["threshold"]
    is_fire = proba >= threshold
    return {
        "fire": bool(is_fire),
        "label": "fire" if is_fire else "no_fire",
        "probability": round(proba, 4),
        "riskBand": _band(proba),
        "threshold": threshold,
        "model": bundle["model_name"],
        "inputs": row,
        "note": "Simulated-data model — research/educational, not certified safety guidance.",
    }


def predict_batch(items: list[dict]) -> list[dict]:
    return [predict(it) for it in items]


def _cli() -> int:
    ap = argparse.ArgumentParser(description="Fire-prediction inference")
    ap.add_argument("--json", help="conditions as a JSON object")
    ap.add_argument("--material")
    ap.add_argument("--material-type", dest="material_type")
    ap.add_argument("--flow-config", dest="flow_configuration")
    ap.add_argument("--o2", type=float, help="oxygen percent")
    ap.add_argument("--pressure", type=float, help="kPa")
    ap.add_argument("--flow", type=float, help="flow velocity cm/s")
    ap.add_argument("--temp", type=float, help="ambient temperature C")
    ap.add_argument("--info", action="store_true", help="print model info and exit")
    args = ap.parse_args()

    if args.info:
        print(json.dumps(model_info(), indent=2))
        return 0

    if args.json:
        conditions = json.loads(args.json)
    else:
        conditions = {k: v for k, v in {
            "material": args.material, "material_type": args.material_type,
            "flow_configuration": args.flow_configuration, "o2": args.o2,
            "pressure": args.pressure, "flow": args.flow, "temp": args.temp,
        }.items() if v is not None}

    print(json.dumps(predict(conditions), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
