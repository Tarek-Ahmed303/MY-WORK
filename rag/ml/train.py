"""Train the fire-prediction model on the project combustion dataset.

Predicts whether a given set of cabin conditions produces a SUSTAINED fire
(steady_spread or flash_fire) vs no sustained fire (extinguished /
self_extinguished). Compares a logistic-regression baseline and a
random-forest, picks the best by cross-validated ROC-AUC, retrains on all
data, and saves a single self-contained artifact (ml/artifacts/fire_model.joblib)
plus a metrics report the teammate can read.

No pandas dependency: features are a numpy object array and the
ColumnTransformer selects columns by index.

Usage:  python ml/train.py        (from the project root)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

from ml.features import (CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES, TARGET,
                         label_fire)

RAW = ROOT / "data" / "raw" / "experiments_raw.json"
ART_DIR = ROOT / "ml" / "artifacts"
MODEL_PATH = ART_DIR / "fire_model.joblib"
METRICS_PATH = ART_DIR / "metrics.json"
RANDOM_STATE = 42

NUM_IDX = [FEATURES.index(f) for f in NUMERIC_FEATURES]
CAT_IDX = [FEATURES.index(f) for f in CATEGORICAL_FEATURES]


def load_xy():
    rows = json.loads(RAW.read_text(encoding="utf-8"))
    X = np.array([[r[f] for f in FEATURES] for r in rows], dtype=object)
    y = np.array([label_fire(r["outcome"]) for r in rows])
    return rows, X, y


def make_pipeline(classifier) -> Pipeline:
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUM_IDX),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_IDX),
    ])
    return Pipeline([("pre", pre), ("clf", classifier)])


def evaluate(name, pipe, X, y) -> dict:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    proba = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]
    pred = (proba >= 0.5).astype(int)
    return {
        "model": name,
        "cv_roc_auc": round(float(roc_auc_score(y, proba)), 4),
        "cv_accuracy": round(float(accuracy_score(y, pred)), 4),
        "cv_precision": round(float(precision_score(y, pred)), 4),
        "cv_recall": round(float(recall_score(y, pred)), 4),
        "cv_f1": round(float(f1_score(y, pred)), 4),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def main() -> int:
    rows, X, y = load_xy()
    print(f"dataset: {len(y)} records | fire={int(y.sum())} no-fire={int((1 - y).sum())} "
          f"({100 * y.mean():.1f}% fire)")

    candidates = {
        "logreg": make_pipeline(LogisticRegression(max_iter=1000, class_weight="balanced",
                                                   random_state=RANDOM_STATE)),
        "random_forest": make_pipeline(RandomForestClassifier(
            n_estimators=300, max_depth=8, min_samples_leaf=3,
            class_weight="balanced", random_state=RANDOM_STATE)),
    }

    results = []
    for name, pipe in candidates.items():
        res = evaluate(name, pipe, X, y)
        results.append(res)
        print(f"  {name:14s} ROC-AUC={res['cv_roc_auc']}  acc={res['cv_accuracy']}  "
              f"P={res['cv_precision']}  R={res['cv_recall']}  F1={res['cv_f1']}")

    best = max(results, key=lambda r: r["cv_roc_auc"])
    best_name = best["model"]
    print(f"best model: {best_name} (CV ROC-AUC {best['cv_roc_auc']})")

    # held-out test report for the model card
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y,
                                           random_state=RANDOM_STATE)
    pipe = make_pipeline(candidates[best_name].named_steps["clf"])
    pipe.fit(Xtr, ytr)
    proba_te = pipe.predict_proba(Xte)[:, 1]
    pred_te = (proba_te >= 0.5).astype(int)
    holdout = {
        "test_size": int(len(yte)),
        "roc_auc": round(float(roc_auc_score(yte, proba_te)), 4),
        "accuracy": round(float(accuracy_score(yte, pred_te)), 4),
        "report": classification_report(yte, pred_te,
                                        target_names=["no_fire", "fire"], output_dict=True),
    }

    # final model trained on ALL data (ship the strongest fit)
    final = make_pipeline(candidates[best_name].named_steps["clf"])
    final.fit(X, y)

    ART_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "pipeline": final,
        "features": FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "target": TARGET,
        "fire_outcomes": ["steady_spread", "flash_fire"],
        "model_name": best_name,
        "sklearn_version": __import__("sklearn").__version__,
        "threshold": 0.5,
    }, MODEL_PATH)

    # permutation importance for interpretability
    try:
        from sklearn.inspection import permutation_importance
        pi = permutation_importance(final, X, y, n_repeats=10,
                                    random_state=RANDOM_STATE, scoring="roc_auc")
        importance = sorted(
            [{"feature": f, "importance": round(float(m), 4)}
             for f, m in zip(FEATURES, pi.importances_mean)],
            key=lambda d: d["importance"], reverse=True)
    except Exception:
        importance = []

    metrics = {
        "dataset": {"n": int(len(y)), "fire": int(y.sum()), "no_fire": int((1 - y).sum()),
                    "fire_pct": round(100 * float(y.mean()), 1)},
        "cross_validation": results,
        "selected_model": best_name,
        "holdout_test": holdout,
        "feature_importance": importance,
        "features": FEATURES,
        "artifact": str(MODEL_PATH.relative_to(ROOT)),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"saved model -> {MODEL_PATH.relative_to(ROOT)}")
    print(f"saved metrics -> {METRICS_PATH.relative_to(ROOT)}")
    print(f"holdout ROC-AUC={holdout['roc_auc']} accuracy={holdout['accuracy']}")
    if importance:
        print("top features:", ", ".join(f"{d['feature']}={d['importance']}"
                                          for d in importance[:4]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
