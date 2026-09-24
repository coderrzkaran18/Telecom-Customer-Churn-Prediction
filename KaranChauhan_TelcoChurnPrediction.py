# ============================================================
#  TELCO CUSTOMER CHURN - MODEL TRAINING & EVALUATION
#  AICTE Data Analytics with AI Internship - Final Project
#  Author: [Your Name]
# ============================================================

import pandas as pd
import numpy as np
import os
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)

# ─────────────────────────────────────────────
# STEP 0: models/ folder banana
# ─────────────────────────────────────────────
os.makedirs("models", exist_ok=True)
print("[OK] 'models/' folder ready hai.\n")

# ─────────────────────────────────────────────
# STEP 1: Dataset Load karna
# ─────────────────────────────────────────────
print("=" * 65)
print("  STEP 1: DATASET LOADING")
print("=" * 65)

df = pd.read_csv("Telco_Churn_Data.csv")
print(f"[OK] Dataset loaded -> Rows: {df.shape[0]}, Cols: {df.shape[1]}")

# ─────────────────────────────────────────────
# STEP 2: Churn (Target) column banana
# EDA se pata chala: tenure <= 12 = Churn 'Yes'
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 2: TARGET COLUMN (Churn) BANANA")
print("=" * 65)

if "Churn" not in df.columns:
    df["Churn"] = df["tenure"].apply(lambda x: "Yes" if x <= 12 else "No")
    print("[INFO] Churn column nahi tha -> tenure <= 12 = 'Yes' proxy banaya")

churn_counts = df["Churn"].value_counts()
print(f"       Churn=Yes : {churn_counts.get('Yes', 0)} ({churn_counts.get('Yes',0)/len(df)*100:.1f}%)")
print(f"       Churn=No  : {churn_counts.get('No',  0)} ({churn_counts.get('No', 0)/len(df)*100:.1f}%)")

# ─────────────────────────────────────────────
# STEP 3: Missing Values Handle karna
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 3: MISSING VALUES CHECK")
print("=" * 65)

missing = df.isnull().sum()
total_missing = missing.sum()
if total_missing == 0:
    print("[OK] Koi missing values nahi hain - dataset clean hai!")
else:
    print(f"[WARN] {total_missing} missing values milein:")
    print(missing[missing > 0])

# ─────────────────────────────────────────────
# STEP 4: Features X aur Target y define karna
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 4: FEATURE SELECTION")
print("=" * 65)

# customerID model ke liye useful nahi hai, drop karo
df.drop(columns=["customerID"], inplace=True)

# Target
y_raw = df["Churn"]
y = (y_raw == "Yes").astype(int)   # 1=Churned, 0=Not Churned

# Features
X = df.drop(columns=["Churn"])

# Categorical aur Numerical columns alag karo
cat_cols = X.select_dtypes(include=["object", "str"]).columns.tolist()
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

print(f"[OK] Features (X) shape : {X.shape}")
print(f"[OK] Target  (y) shape  : {y.shape}")
print(f"\n     Numerical columns  ({len(num_cols)}): {num_cols}")
print(f"     Categorical columns ({len(cat_cols)}): {cat_cols}")

# ─────────────────────────────────────────────
# STEP 5: Train / Test Split (80/20)
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 5: TRAIN / TEST SPLIT (80/20, stratified)")
print("=" * 65)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"[OK] Training set   : {X_train.shape[0]} rows")
print(f"[OK] Test set       : {X_test.shape[0]} rows")

# ─────────────────────────────────────────────
# STEP 6: Preprocessing Pipeline banana
# ─────────────────────────────────────────────
# Numerical  -> Missing impute (median) + StandardScaler
# Categorical-> Missing impute (most_frequent) + OneHotEncoding

num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler()),
])

cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot",  OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer(transformers=[
    ("num", num_transformer, num_cols),
    ("cat", cat_transformer, cat_cols),
])

# ─────────────────────────────────────────────
# STEP 7: Models Define karna (3 models)
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 6: MODEL DEFINITION (3 models)")
print("=" * 65)

models = {
    "Logistic Regression": Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            max_iter=1000, random_state=42, class_weight="balanced"
        )),
    ]),
    "Random Forest": Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200, max_depth=10,
            random_state=42, class_weight="balanced", n_jobs=-1
        )),
    ]),
    "Gradient Boosting": Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", GradientBoostingClassifier(
            n_estimators=200, learning_rate=0.1,
            max_depth=4, random_state=42
        )),
    ]),
}

print(f"[OK] 3 models ready hain: {list(models.keys())}")

# ─────────────────────────────────────────────
# STEP 8: Train + Evaluate har model
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 7: TRAINING & EVALUATION")
print("=" * 65)

results = {}

for name, pipeline in models.items():
    print(f"\n  >> Training: {name} ...")

    # --- Train ---
    pipeline.fit(X_train, y_train)

    # --- Predict ---
    y_pred      = pipeline.predict(X_test)
    y_pred_prob = pipeline.predict_proba(X_test)[:, 1]

    # --- Metrics ---
    acc       = accuracy_score (y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall    = recall_score   (y_test, y_pred, zero_division=0)
    f1        = f1_score       (y_test, y_pred, zero_division=0)
    roc_auc   = roc_auc_score  (y_test, y_pred_prob)
    cm        = confusion_matrix(y_test, y_pred)

    results[name] = {
        "Accuracy" : round(acc,      4),
        "Precision": round(precision, 4),
        "Recall"   : round(recall,    4),
        "F1-Score" : round(f1,        4),
        "ROC-AUC"  : round(roc_auc,   4),
        "pipeline" : pipeline,
        "cm"       : cm,
    }

    print(f"     Accuracy  : {acc:.4f}")
    print(f"     Precision : {precision:.4f}")
    print(f"     Recall    : {recall:.4f}")
    print(f"     F1-Score  : {f1:.4f}")
    print(f"     ROC-AUC   : {roc_auc:.4f}")
    print(f"     Confusion Matrix:")
    print(f"       [[TN={cm[0,0]}  FP={cm[0,1]}]")
    print(f"        [FN={cm[1,0]}  TP={cm[1,1]}]]")
    print(f"     Classification Report:")
    print(classification_report(y_test, y_pred,
                                 target_names=["No Churn", "Churn"],
                                 zero_division=0))

# ─────────────────────────────────────────────
# STEP 9: Comparison Table print karna
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 8: MODEL COMPARISON TABLE")
print("=" * 65)

# Sirf metrics wala dict banao (pipeline hata ke)
metrics_only = {
    name: {k: v for k, v in vals.items() if k not in ("pipeline", "cm")}
    for name, vals in results.items()
}
comparison_df = pd.DataFrame(metrics_only).T
comparison_df = comparison_df.sort_values("ROC-AUC", ascending=False)

print(comparison_df.to_string())

# ─────────────────────────────────────────────
# STEP 10: Best Model select karna
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 9: BEST MODEL SELECTION")
print("=" * 65)

best_model_name = comparison_df.index[0]
best_metrics    = comparison_df.iloc[0]
best_pipeline   = results[best_model_name]["pipeline"]

print(f"\n  WINNER -> {best_model_name}")
print(f"  ROC-AUC  : {best_metrics['ROC-AUC']}")
print(f"  F1-Score : {best_metrics['F1-Score']}")
print(f"  Accuracy : {best_metrics['Accuracy']}")

print(f"""
  WHY {best_model_name}?
  ------------------------------------------------
  ROC-AUC sabse zyada hai -> model churn aur
  non-churn customers ke beech best discrimination
  karta hai.

  Churn prediction mein ROC-AUC aur Recall
  sabse important metrics hain kyunki:
  - False Negatives (miss kiye gaye churners) zyada
    costly hote hain business ke liye.
  - Isliye high Recall wala model prefer kiya jaata hai.
""")

# ─────────────────────────────────────────────
# STEP 11: Best Model Save karna
# ─────────────────────────────────────────────
print("=" * 65)
print("  STEP 10: MODEL SAVE KARNA")
print("=" * 65)

model_path = os.path.join("models", "best_churn_model.pkl")
joblib.dump(best_pipeline, model_path)
print(f"[OK] Best model saved -> {model_path}")
print(f"     Model type: {best_model_name}")
print(f"     File size : {os.path.getsize(model_path) / 1024:.1f} KB")

# Column order bhi save karo (Streamlit app ke liye zaruri)
feature_meta = {
    "feature_columns": list(X.columns),
    "cat_cols"        : cat_cols,
    "num_cols"        : num_cols,
    "best_model_name" : best_model_name,
}
joblib.dump(feature_meta, os.path.join("models", "feature_meta.pkl"))
print(f"[OK] Feature metadata saved -> models/feature_meta.pkl")

print("\n" + "=" * 65)
print("  [OK] MODEL TRAINING COMPLETE!")
print("  Best model & metadata dono 'models/' folder mein save hain.")
print("  Next step -> python app.py  (Streamlit UI)")
print("=" * 65)
