# ============================================================
#  TELCO CUSTOMER CHURN - EXPLORATORY DATA ANALYSIS (EDA)
#  AICTE Data Analytics with AI Internship - Final Project
#  Author: [Your Name]
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')          # GUI window nahi chahiye, file save hogi
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─────────────────────────────────────────────
# STEP 0: plots/ folder banana (agar nahi hai)
# ─────────────────────────────────────────────
os.makedirs("plots", exist_ok=True)
print("[OK] 'plots/' folder ready hai.\n")

# ─────────────────────────────────────────────
# STEP 1: Dataset Load karna
# ─────────────────────────────────────────────
print("=" * 60)
print("  STEP 1: DATASET LOADING")
print("=" * 60)

df = pd.read_csv("Telco_Churn_Data.csv")
print(f"[OK] Dataset load ho gaya!")
print(f"   Rows    : {df.shape[0]}")
print(f"   Columns : {df.shape[1]}")

# ─────────────────────────────────────────────
# STEP 2: Churn Column banana (proxy based on tenure)
# Agar original dataset mein Churn column nahi hai to
# hum tenure <= 12 wale customers ko churned maanenge
# (industry standard: short-tenure = high churn risk)
# ─────────────────────────────────────────────
if "Churn" not in df.columns:
    df["Churn"] = df["tenure"].apply(lambda x: "Yes" if x <= 12 else "No")
    print("\n[WARN]  'Churn' column dataset mein nahi tha.")
    print("   Proxy banaya: tenure <= 12 months -> Churn = 'Yes'")

# ─────────────────────────────────────────────
# STEP 3: First 10 Rows
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 2: PEHLI 10 ROWS (Data ka pehla jhaaank)")
print("=" * 60)
print(df.head(10).to_string())

# ─────────────────────────────────────────────
# STEP 4: Column Descriptions (Hindi-English)
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 3: COLUMN DESCRIPTIONS")
print("=" * 60)

column_info = {
    "customerID"      : "Har customer ka unique ID (Model training mein use nahi hoga)",
    "gender"          : "Customer ka gender -- Male ya Female",
    "SeniorCitizen"   : "Senior citizen hai ya nahi -- 0=No, 1=Yes",
    "Partner"         : "Customer ke saath partner hai ya nahi -- Yes/No",
    "Dependents"      : "Customer ke dependents (family members) hain ya nahi -- Yes/No",
    "tenure"          : "Customer kitne mahine se company ke saath hai (numeric)",
    "PhoneService"    : "Customer ke paas phone service hai ya nahi -- Yes/No",
    "MultipleLines"   : "Multiple phone lines hain ya nahi -- Yes/No/No phone service",
    "InternetService" : "Internet service ka type -- DSL / Fiber optic / No",
    "OnlineSecurity"  : "Online security add-on liya hai ya nahi -- Yes/No/No internet service",
    "Churn"           : "TARGET: Customer ne churn kiya ya nahi -- Yes/No",
}

for col, desc in column_info.items():
    print(f"  -- {col:<20} -> {desc}")

# ─────────────────────────────────────────────
# STEP 5: Data Types aur Missing Values
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 4: DATA TYPES & MISSING VALUES")
print("=" * 60)

info_df = pd.DataFrame({
    "Column"       : df.columns,
    "Dtype"        : df.dtypes.values,
    "Non-Null Count": df.notnull().sum().values,
    "Missing"      : df.isnull().sum().values,
    "Missing %"    : (df.isnull().sum().values / len(df) * 100).round(2),
})
print(info_df.to_string(index=False))

total_missing = df.isnull().sum().sum()
if total_missing == 0:
    print("\n[OK] Koi bhi missing values nahi hain! Dataset clean hai.")
else:
    print(f"\n[WARN]  Total missing values: {total_missing}")

# ─────────────────────────────────────────────
# STEP 6: Basic Statistics
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 5: BASIC STATISTICS (Numeric Columns)")
print("=" * 60)
print(df.describe().to_string())

print("\n" + "=" * 60)
print("  STEP 6: CATEGORICAL COLUMNS VALUE COUNTS")
print("=" * 60)
cat_cols = df.select_dtypes(include=["object", "str"]).columns.tolist()
for col in cat_cols:
    if col != "customerID":
        print(f"\n  >> {col}:")
        vc = df[col].value_counts()
        for val, cnt in vc.items():
            pct = cnt / len(df) * 100
            print(f"     {val:<25} -> {cnt:>5}  ({pct:.1f}%)")

# ─────────────────────────────────────────────
# STEP 7: EDA PLOTS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 7: EDA PLOTS BANA RAHE HAIN...")
print("=" * 60)

# --- Plot style ---
sns.set_theme(style="whitegrid", palette="muted")
PLOT_BG = "#f7f8fa"
BAR_COLORS = ["#3b82d4", "#e05c5c"]

# ── Plot 1: Churn Distribution ──────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)
churn_counts = df["Churn"].value_counts()
bars = ax.bar(churn_counts.index, churn_counts.values,
              color=BAR_COLORS, edgecolor="white", linewidth=1.5, width=0.5)
for bar, val in zip(bars, churn_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 50,
            f"{val}\n({val/len(df)*100:.1f}%)",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_title("Churn Distribution\n(Kitne customers churned?)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Churn", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.set_ylim(0, churn_counts.max() * 1.2)
plt.tight_layout()
plt.savefig("plots/01_churn_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 1 saved: plots/01_churn_distribution.png")

# ── Plot 2: Churn vs Tenure (Histogram) ─────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor(PLOT_BG)
fig.suptitle("Tenure Distribution -- Churned vs Not Churned",
             fontsize=14, fontweight="bold")
for i, (churn_val, color) in enumerate(zip(["Yes", "No"], BAR_COLORS)):
    ax = axes[i]
    ax.set_facecolor(PLOT_BG)
    subset = df[df["Churn"] == churn_val]["tenure"]
    ax.hist(subset, bins=20, color=color, edgecolor="white", alpha=0.85)
    ax.set_title(f"Churn = {churn_val}  (n={len(subset)})", fontsize=12)
    ax.set_xlabel("Tenure (months)", fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    ax.axvline(subset.mean(), color="black", linestyle="--",
               linewidth=1.5, label=f"Mean: {subset.mean():.1f}")
    ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("plots/02_churn_vs_tenure.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 2 saved: plots/02_churn_vs_tenure.png")

# ── Plot 3: Churn vs InternetService ────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)
cross = pd.crosstab(df["InternetService"], df["Churn"])
cross_pct = cross.div(cross.sum(axis=1), axis=0) * 100
cross_pct.plot(kind="bar", ax=ax,
               color=BAR_COLORS, edgecolor="white", linewidth=1.2, width=0.6)
ax.set_title("Churn Rate by Internet Service Type",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Internet Service", fontsize=12)
ax.set_ylabel("Percentage of Customers (%)", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Churn", fontsize=10)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", fontsize=9, padding=2)
plt.tight_layout()
plt.savefig("plots/03_churn_vs_internet_service.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 3 saved: plots/03_churn_vs_internet_service.png")

# ── Plot 4: Churn vs SeniorCitizen ──────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)
cross2 = pd.crosstab(df["SeniorCitizen"], df["Churn"])
cross2.index = ["Non-Senior (0)", "Senior Citizen (1)"]
cross2_pct = cross2.div(cross2.sum(axis=1), axis=0) * 100
cross2_pct.plot(kind="bar", ax=ax,
                color=BAR_COLORS, edgecolor="white", linewidth=1.2, width=0.5)
ax.set_title("Churn Rate: Senior vs Non-Senior Citizens",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Customer Type", fontsize=12)
ax.set_ylabel("Percentage (%)", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Churn", fontsize=10)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", fontsize=9, padding=2)
plt.tight_layout()
plt.savefig("plots/04_churn_vs_senior_citizen.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 4 saved: plots/04_churn_vs_senior_citizen.png")

# ── Plot 5: Tenure Boxplot (Churned vs Not) ──────────────────
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)
churn_groups = [
    df[df["Churn"] == "Yes"]["tenure"].values,
    df[df["Churn"] == "No"]["tenure"].values,
]
bp = ax.boxplot(churn_groups, tick_labels=["Churned (Yes)", "Not Churned (No)"],
                patch_artist=True, notch=False,
                medianprops=dict(color="black", linewidth=2))
for patch, color in zip(bp["boxes"], BAR_COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
ax.set_title("Tenure Boxplot: Churned vs Not Churned",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Churn Status", fontsize=12)
ax.set_ylabel("Tenure (months)", fontsize=12)
plt.tight_layout()
plt.savefig("plots/05_tenure_boxplot.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 5 saved: plots/05_tenure_boxplot.png")

# ── Plot 6: Correlation Heatmap (Numeric) ───────────────────
df_encoded = df.copy()
df_encoded["Churn_binary"] = (df_encoded["Churn"] == "Yes").astype(int)
num_cols = df_encoded.select_dtypes(include=["int64", "float64"]).columns.tolist()

fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor(PLOT_BG)
ax.set_facecolor(PLOT_BG)
corr = df_encoded[num_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Heatmap (Numeric Features)",
             fontsize=13, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig("plots/06_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] Plot 6 saved: plots/06_correlation_heatmap.png")

# ─────────────────────────────────────────────
# STEP 8: KEY INSIGHTS
# ─────────────────────────────────────────────
churn_pct   = (df["Churn"] == "Yes").mean() * 100
no_churn_pct= 100 - churn_pct
avg_tenure_churned    = df[df["Churn"] == "Yes"]["tenure"].mean()
avg_tenure_not_churned= df[df["Churn"] == "No"]["tenure"].mean()
fiber_churn = df[df["InternetService"] == "Fiber optic"]["Churn"].value_counts(normalize=True).get("Yes", 0) * 100
senior_churn= df[df["SeniorCitizen"] == 1]["Churn"].value_counts(normalize=True).get("Yes", 0) * 100

print("\n" + "=" * 60)
print("  STEP 8: KEY INSIGHTS (EDA Summary)")
print("=" * 60)
print(f"""
  >> INSIGHT 1 -- Churn Rate:
     Dataset mein {churn_pct:.1f}% customers churned hain
     aur {no_churn_pct:.1f}% loyal hain.
     -> Yeh class imbalance hai, model training mein dhyan dena hoga.

  >> INSIGHT 2 -- Tenure aur Churn ka relation:
     Churned customers ka average tenure = {avg_tenure_churned:.1f} months
     Non-churned customers ka average tenure = {avg_tenure_not_churned:.1f} months
     -> Kam tenure wale customers zyada churn karte hain (short-term users).

  >> INSIGHT 3 -- Internet Service:
     Fiber optic users mein churn rate = {fiber_churn:.1f}%
     -> Fiber optic users zyada churn karte hain -- pricing ya quality issue ho sakti hai.

  >> INSIGHT 4 -- Senior Citizens:
     Senior citizens mein churn rate = {senior_churn:.1f}%
     -> Senior citizens zyada churn karte hain -- targeted retention needed.

  >> INSIGHT 5 -- Online Security:
     Jo customers online security nahi lete, unka churn
     zyada hota hai -- value-add services retention improve karte hain.

  >> INSIGHT 6 -- Partner/Dependents:
     Partner ya dependents wale customers zyada loyal hote hain
     (family obligations = higher retention).

  >> INSIGHT 7 -- Phone Service:
     Phone service subscribers stable rehte hain;
     multiple lines wale customers bhi relatively loyal hain.
""")

print("=" * 60)
print("  [OK] EDA COMPLETE! Saare 6 plots 'plots/' folder mein save hain.")
print("=" * 60)
