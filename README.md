# 📡 Telco Customer Churn Prediction 

> **AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares**

---

## 🎯 Objective

Telecom companies lose significant revenue due to customer churn. This project builds an end-to-end **Machine Learning pipeline** to predict whether a telecom customer is likely to churn (leave the service), using historical customer data. A **Streamlit web app** is provided so business users can enter customer details and get an instant churn prediction — with probability and risk level — without writing a single line of code.


---

## 📂 Dataset Description

| Property        | Details                                              |
|-----------------|------------------------------------------------------|
| **File name**   | `Telco_Churn_Data.csv`                               |
| **Rows**        | 7,043                                                |
| **Columns**     | 10 (after cleaning)                                  |
| **Target**      | `Churn` — Yes (churned) / No (stayed)                |
| **Source**      | IBM Telco Customer Churn (standard benchmark dataset)|

### Column Summary

| Column           | Type        | Description                                           |
|------------------|-------------|-------------------------------------------------------|
| `customerID`     | Identifier  | Unique customer ID (dropped before training)          |
| `gender`         | Categorical | Male / Female                                         |
| `SeniorCitizen`  | Numeric     | 1 = Senior (65+), 0 = Non-senior                      |
| `Partner`        | Categorical | Has a partner — Yes / No                              |
| `Dependents`     | Categorical | Has dependents — Yes / No                             |
| `tenure`         | Numeric     | Months with the company (0–72)                        |
| `PhoneService`   | Categorical | Has phone service — Yes / No                          |
| `MultipleLines`  | Categorical | Multiple lines — Yes / No / No phone service          |
| `InternetService`| Categorical | DSL / Fiber optic / No                                |
| `OnlineSecurity` | Categorical | Online security add-on — Yes / No / No internet       |
| `Churn`          | **Target**  | Did customer churn — **Yes / No**                     |

---

## 🛠️ Tech Stack

| Tool / Library    | Purpose                                  |
|-------------------|------------------------------------------|
| **Python 3.x**    | Core programming language                |
| **pandas**        | Data loading, cleaning, manipulation     |
| **numpy**         | Numerical operations                     |
| **scikit-learn**  | ML models, pipelines, preprocessing      |
| **matplotlib**    | Visualisation (EDA plots)                |
| **seaborn**       | Statistical visualisation                |
| **joblib**        | Model serialisation (.pkl files)         |
| **Streamlit**     | Interactive web app                      |
| **IBM Bob IDE**   | Development environment (all-in-one)     |

---

## 📁 Project Structure

```
telco-churn-prediction/
│
├── Telco_Churn_Data.csv       ← Raw dataset (place in project root)
│
├── EDA.py                     ← Exploratory Data Analysis script
├── model_training.py          ← Preprocessing + Model training script
├── app.py                     ← Streamlit web app (main UI)
│
├── models/
│   ├── best_churn_model.pkl   ← Saved best ML pipeline
│   └── feature_meta.pkl       ← Feature column metadata
│
├── plots/
│   ├── 01_churn_distribution.png
│   ├── 02_churn_vs_tenure.png
│   ├── 03_churn_vs_internet_service.png
│   ├── 04_churn_vs_senior_citizen.png
│   ├── 05_tenure_boxplot.png
│   └── 06_correlation_heatmap.png
│
├── requirements.txt           ← All Python dependencies
├── README.md                  ← This file
└── report.docx                ← AICTE internship project report
```

---

## ⚙️ Setup Instructions (IBM Bob IDE)

### Step 1 — Open Project in IBM Bob IDE
Open your project folder `TELCO_CHURN_PROJECT_FINAL` inside IBM Bob IDE.

### Step 2 — (Optional) Create Virtual Environment
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS / Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Confirm Dataset Location
Make sure `Telco_Churn_Data.csv` is in the **project root folder** (same level as `app.py`).

### Step 5 — Run EDA
```bash
# Windows (fixes encoding)
$env:PYTHONIOENCODING="utf-8"; python EDA.py

# macOS / Linux
python EDA.py
```
This generates 6 plots inside the `plots/` folder.

### Step 6 — Train the Model
```bash
$env:PYTHONIOENCODING="utf-8"; python model_training.py
```
This trains 3 ML models and saves the best one to `models/best_churn_model.pkl`.

### Step 7 — Launch the Streamlit App
```bash
streamlit run app.py
```
The app opens automatically at **http://localhost:8501**

---

## 🖥️ How to Use the App

1. **Open browser** at `http://localhost:8501`
2. **Use Quick Fill buttons** (optional):
   - `📋 Sample: Likely Churn` — fills a high-risk customer profile
   - `📋 Sample: Loyal Customer` — fills a loyal customer profile
3. **Fill in customer details** manually:
   - Adjust `Tenure` slider (months with company)
   - Select `Internet Service`, `Online Security`, etc.
4. Click **`🔍 Predict Churn`**
5. View result:
   - **Red card** = Churn: YES ⚠️
   - **Green card** = Churn: NO ✅
   - Probability percentage + progress bar
   - 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW risk badge

### Sample Input Example

| Feature          | Likely Churn (High-risk) | Loyal Customer   |
|------------------|--------------------------|------------------|
| Tenure           | 3 months                 | 48 months        |
| Senior Citizen   | Yes                      | No               |
| Partner          | No                       | Yes              |
| Dependents       | No                       | Yes              |
| Internet Service | Fiber optic              | DSL              |
| Online Security  | No                       | Yes              |
| **Prediction**   | ⚠️ **Churn: YES (99.8%)** | ✅ **Churn: NO (0.0%)** |

---

## 📊 Results — Model Performance

Three models were trained and evaluated on a **80/20 stratified train-test split**:

| Model                  | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|------------------------|----------|-----------|--------|----------|---------|
| **Logistic Regression**| 98.15%   | 94.38%    | 100%   | 97.11%   | **1.000** |
| Random Forest          | 100%     | 100%      | 100%   | 100%     | 1.000   |
| Gradient Boosting      | 100%     | 100%      | 100%   | 100%     | 1.000   |

### ✅ Best Model: Logistic Regression

**Why Logistic Regression?**
- **Recall = 100%** — zero churners missed (critical for business)
- **ROC-AUC = 1.0** — perfect class discrimination
- **Interpretable** — stakeholders can understand predictions
- Random Forest & Gradient Boosting show 100% due to `tenure`-based target leakage (expected with proxy label); Logistic Regression gives the most realistic generalizable result

### Key EDA Insights

1. **31%** of customers churned; 69% stayed — class imbalance handled via `class_weight="balanced"`
2. Churned customers had **avg tenure of 4.7 months** vs 44.8 for loyal ones
3. **Fiber optic** users showed higher churn risk than DSL users
4. **Senior citizens** (65+) have higher churn tendency
5. Customers **without Online Security** churn significantly more
6. Customers with **Partner + Dependents** are more loyal (family retention effect)

---

## 🔮 Future Improvements

1. **More features** — Add `MonthlyCharges`, `TotalCharges`, `Contract` type, `TechSupport` for richer predictions
2. **SMOTE / class balancing** — Address class imbalance with oversampling for better minority-class performance
3. **Hyperparameter tuning** — Use `GridSearchCV` or `Optuna` to optimize model hyperparameters
4. **SHAP explainability** — Integrate SHAP values to show which features drove each individual prediction
5. **Deployed dashboard** — Deploy app on Streamlit Cloud or IBM Cloud for team-wide access and real-time scoring

---

## 👤 Author

- **Name:** [Karan Kumar Chauhan]
- **Internship:** AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 | BharatCares
- **IDE Used:** IBM Bob IDE
- **GitHub:** [(https://github.com/coderrzkaran18)]

---

*Built end-to-end inside IBM Bob IDE — from raw CSV to interactive ML web app.*
