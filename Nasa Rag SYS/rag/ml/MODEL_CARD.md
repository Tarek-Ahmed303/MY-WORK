# ML Fire-Prediction Model — handoff for integration

A **standalone, trained** scikit-learn model that predicts whether a set of cabin
conditions will produce a **sustained fire**. Nothing in the RAG/retrieval stack is
required — load the artifact, call `predict()`, done.

> Research/educational model trained on the project's **simulated** combustion dataset (modeled on NASA microgravity investigations). Not certified safety guidance.

---

## What it predicts

Binary classification:

| Label | Meaning | Dataset outcomes |
|---|---|---|
| `fire` (1) | A sustained fire develops | `steady_spread`, `flash_fire` |
| `no_fire` (0) | Flame does not sustain | `extinguished`, `self_extinguished` |

Dataset: 300 records, 63% fire / 37% no-fire.

## Inputs (pre-test cabin conditions only — no leakage)

| Feature | Type | Example | Notes |
|---|---|---|---|
| `oxygen_concentration_pct` | number | 19.0 | **dominant driver** |
| `pressure_kpa` | number | 101.3 | |
| `flow_velocity_cm_s` | number | 6.0 | imposed oxidizer flow |
| `ambient_temperature_c` | number | 24 | |
| `material` | string | `PMMA (acrylic)` | one of the 7 dataset materials |
| `material_type` | string | `solid` | inferred from `material` if omitted |
| `flow_configuration` | string | `concurrent` | `concurrent`/`opposed`/`quiescent`/`forced_flow` |

**Deliberately excluded** (they are results, not conditions — using them would leak the answer): `ignition_time_s`, `flame_spread_rate_mm_s`, `heat_release_rate_kw`, `soot_volume_fraction_ppm`, `risk_score`, `risk_level`, `outcome`.

Aliases accepted by `predict()` / the API: `o2`→oxygen, `flow`/`flow_cm_s`→flow velocity, `pressure`→pressure, `temp`→temperature. Missing fields fall back to cabin-nominal defaults; `material_type` is inferred from `material`.

## Quality (cross-validated, see `ml/artifacts/metrics.json`)

Selected model: **RandomForest** (beat the logistic-regression baseline).

| Metric | 5-fold CV | 25% holdout |
|---|---|---|
| ROC-AUC | 0.989 | 0.999 |
| Accuracy | 0.95 | 0.987 |
| Precision / Recall / F1 | 0.95 / 0.97 / 0.96 | — |

Top feature by permutation importance: **oxygen concentration** (by far), then pressure — consistent with the dataset's physics (flames extinguish below ~15% O₂).

## Files

```
ml/
├── features.py              # feature list, label rule, input normalization (shared contract)
├── train.py                 # trains, cross-validates, picks best, saves artifact + metrics
├── predict.py               # predict(dict) + predict_batch() + CLI  ← import this
├── artifacts/
│   ├── fire_model.joblib     # the trained pipeline (preprocessing + classifier in one object)
│   └── metrics.json          # full metrics report
└── MODEL_CARD.md            # this file
```

## Use it — three ways

### 1) Python import (recommended for integration)
```python
from ml.predict import predict

predict({
    "material": "PMMA (acrylic)",
    "oxygen_concentration_pct": 19.0,
    "pressure_kpa": 101.3,
    "flow_velocity_cm_s": 6.0,
    "ambient_temperature_c": 24,
})
# {"fire": True, "label": "fire", "probability": 0.87, "riskBand": "HIGH",
#  "threshold": 0.5, "model": "random_forest", "inputs": {...}, "note": "..."}
```
`predict_batch([...])` scores a list. The artifact loads once and is cached.

### 2) CLI
```bash
python ml/predict.py --material "PMMA (acrylic)" --o2 19 --flow 6 --pressure 101.3 --temp 24
python ml/predict.py --json '{"material":"Nomex","o2":13.5}'
python ml/predict.py --info          # model metadata
```

### 3) HTTP (optional convenience endpoints, already wired into the backend)
```
POST /ml/predict      body: {"material":"PMMA (acrylic)","oxygen_concentration_pct":19,"flow_velocity_cm_s":6}
GET  /ml/info
```
Auth: `X-API-Key` or Bearer (same as other mobile endpoints). Returns the same dict as `predict()`. If the artifact is missing you get 503 `ML_NOT_TRAINED`.

## Retraining
```bash
python ml/train.py        # re-reads data/raw/experiments_raw.json, re-selects, re-saves
```
The data pipeline, retrieval and risk model are untouched by this — the model is fully independent. If you add data, re-run train and the test `tests/test_ml_model.py::test_quality_threshold` guards against a quality regression.

## Output contract (stable)
```json
{
  "fire": true,
  "label": "fire",
  "probability": 0.87,
  "riskBand": "HIGH",     // >=0.66 HIGH, >=0.33 MED, else LOW
  "threshold": 0.5,
  "model": "random_forest",
  "inputs": { "...": "the normalized features actually used" },
  "note": "Simulated-data model — research/educational, not certified safety guidance."
}
```

## How this differs from the existing `/risk` endpoints
- `/risk*` (the app's risk model) is a transparent nearest-neighbor + linear blend producing a 0–100 **risk index** for the live dashboard.
- This ML model is a **trained classifier** producing a calibrated **fire probability** and a yes/no decision. It's what your teammate asked for as a separate, model-based component. Both are grounded in the same dataset and agree directionally (oxygen dominates both).
