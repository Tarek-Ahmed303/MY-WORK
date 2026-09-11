# 🧍 Body Language Analysis — XGBoost Model

## 📌 Overview

This project implements a **Machine Learning model for body language analysis** using **XGBoost (Extreme Gradient Boosting)**.

The model analyzes numerical body-language features extracted from human pose/keypoint data and predicts the corresponding **body language behavior/class**.

This model is designed as a component of an **AI-powered Online Interview System**, where body posture and movement can be analyzed to provide feedback about a candidate's non-verbal communication.

---

## 🎯 Project Objective

The main objective is to automatically analyze body posture and movement during an interview and identify behavioral patterns that may provide useful feedback to the candidate.

The system focuses on features such as:

* Shoulder position and alignment
* Wrist position
* Eye and head relationships
* Body lean
* Spine angle
* Shoulder and hip positioning
* Head tilt
* Eye distance
* Relative body proportions

The extracted features are provided to an XGBoost classifier for prediction.

---

## 🤖 Why XGBoost?

**XGBoost** is a gradient-boosting framework based on decision trees. It builds an ensemble of trees sequentially, with later trees learning from errors made by previous trees.

It is particularly effective for **structured/tabular data**, making it a strong choice for body-language features represented as numerical values rather than raw images.

### Advantages

* High performance on tabular data
* Handles nonlinear relationships between features
* Effective with relatively small and medium-sized datasets
* Includes regularization to reduce overfitting
* Supports multiclass classification
* Fast and computationally efficient
* Provides feature-importance information

---

## 📊 Input Features

The model uses engineered body-language features including:

```text
eye_shoulder_y_ratio
shoulder_y_diff
wrist_distance_x
wrist_shoulder_ratio
nose_eye_center_offset_x
shoulder_span
hip_shoulder_y_diff
body_lean_x
shoulder_center_x
hip_center_x
spine_angle
eye_distance
head_tilt_angle
eye_distance_ratio
```

These features represent geometric relationships between different body landmarks.

Using ratios, distances, angles, and relative positions helps the model focus on **body configuration and movement patterns** rather than relying directly on raw pixel values.

---

## 🔄 Processing Pipeline

The overall pipeline is:

```text
Camera / Video
      ↓
Pose / Landmark Detection
      ↓
Body Landmark Coordinates
      ↓
Feature Engineering
      ↓
Numerical Body-Language Features
      ↓
XGBoost Classifier
      ↓
Predicted Body Language Class
      ↓
Interview Feedback
```

---

## 🧠 Model Architecture

Unlike CNN-based image classifiers, this model does not directly process images.

Instead, the system converts body landmarks into structured numerical features.

The XGBoost model then learns decision boundaries between different body-language classes.

Conceptually:

```text
Input Features
      │
      ├── Body Position
      ├── Shoulder Relationships
      ├── Wrist Relationships
      ├── Head Position
      ├── Eye Relationships
      └── Body Angles
              │
              ▼
       XGBoost Classifier
              │
              ▼
       Predicted Class
```

For multiclass classification, XGBoost supports multiclass objectives such as `multi:softmax` and probability-based `multi:softprob`.

---

## 📈 Model Performance

The XGBoost model achieved approximately:

**Validation Accuracy: ~95%**

> The exact performance depends on the dataset split, preprocessing, feature engineering, and hyperparameters used during training.

Accuracy should be evaluated on a validation/test set that was not used to train the model.

Recommended additional evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

---

## 🛠️ Technologies Used

* Python
* XGBoost
* Scikit-learn
* NumPy
* Pandas
* OpenCV
* Pose/Landmark Detection
* Matplotlib / Seaborn

---

## 📂 Project Structure

```text
Body_Language/
│
├── README.md
├── model/
│   └── xgboost_body_language_model.pkl
│
├── notebooks/
│   └── body_language_training.ipynb
│
├── data/
│   └── body_language_dataset.csv
│
└── inference/
    └── predict.py
```

*The exact structure may vary depending on the final project implementation.*

---

## 🚀 Training

A simplified example of the training process:

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)
```

The trained model can then be evaluated using the validation/test dataset.

---

## 🔍 Prediction

Once trained, the model receives the engineered body-language features:

```python
prediction = model.predict(X_new)
```

The predicted class can then be converted into a human-readable behavior label.

Example:

```text
Body Features
      ↓
XGBoost
      ↓
"Confident Posture"
```

---

## 💾 Model Saving

The trained model can be saved for later use:

```python
import joblib

joblib.dump(model, "xgboost_body_language_model.pkl")
```

And loaded again with:

```python
model = joblib.load(
    "xgboost_body_language_model.pkl"
)
```

---

## 🔬 Feature Importance

One useful advantage of tree-based models is that feature importance can be examined to understand which body-language measurements contribute most to the predictions.

For example:

```python
import matplotlib.pyplot as plt
from xgboost import plot_importance

plot_importance(model)
plt.show()
```

This can help determine which body-language characteristics are most informative for the classification task.

---

## ⚠️ Important Considerations

Body language is highly dependent on:

* Cultural differences
* Individual behavior
* Camera position
* Camera angle
* Lighting
* Occlusion
* Sitting position
* Body movement
* Interview context

Therefore, the model's prediction should be treated as **behavioral analysis rather than a definitive psychological judgment**.

The system should provide interview feedback based on observable movement and posture patterns rather than claiming to determine a person's personality or intentions.

---

## 🎤 Intended Application

This model is designed to be integrated into an **AI Online Interview Coach**.

A complete interview-analysis system can combine:

```text
                    AI Interview Coach
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Body Language    Facial Expression    Voice Analysis
      XGBoost            Model              Model
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Overall Analysis
                           │
                           ▼
                   Interview Feedback
```

The Body Language module can therefore work alongside facial-expression and vocal-analysis components to provide a more comprehensive interview analysis system.

---

## 📚 References

* XGBoost Documentation: [XGBoost Documentation](https://xgboost.readthedocs.io/en/stable/?utm_source=chatgpt.com)
* XGBoost Parameters: [XGBoost Parameters](https://xgboost.readthedocs.io/en/stable/parameter.html?utm_source=chatgpt.com)

---

## 👨‍💻 Project

**Graduation Project — AI Online Interview System**

**Module:** Body Language Analysis
**Model:** XGBoost
**Task:** Body Language Classification

