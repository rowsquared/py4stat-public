"""prepare_data.py — build analysis-ready tables for the Quarto report."""

from pathlib import Path
import pandas as pd
import numpy as np

# ── paths ────────────────────────────────────────────────────────────
DATA_DIR = Path("/srv/shared/IHS5_sample")
OUT_DIR  = Path("../../../data/1_cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── load source data ─────────────────────────────────────────────────
hh     = pd.read_stata(DATA_DIR / "hh_mod_a_filt.dta", convert_categoricals=True)
roster = pd.read_stata(DATA_DIR / "HH_MOD_B.dta",      convert_categoricals=True)
edu    = pd.read_stata(DATA_DIR / "HH_MOD_C.dta",       convert_categoricals=True,
                       columns=["case_id", "PID", "hh_c08", "hh_c09"])
cons   = pd.read_stata(DATA_DIR / "ihs5_consumption_aggregate.dta",
                       convert_categoricals=True)

print("Loaded shapes:")
for name, df in [("hh", hh), ("roster", roster), ("edu", edu), ("cons", cons)]:
    print(f"  {name:8s} {df.shape}")

# ── 1. Population pyramid table ─────────────────────────────────────
roster = roster.rename(columns={"hh_b03": "sex", "hh_b05a": "age"})
roster["age_band"] = pd.cut(
    roster["age"],
    bins=list(range(0, 85, 5)) + [120],
    labels=[f"{i}-{i+4}" for i in range(0, 80, 5)] + ["80+"],
    right=False,
)
pyramid = (
    roster
    .dropna(subset=["sex", "age_band"])
    .groupby(["age_band", "sex"], observed=True)
    .size()
    .reset_index(name="count")
)
pyramid.to_parquet(OUT_DIR / "pyramid.parquet", index=False)
print("\n✓ pyramid.parquet saved")

# ── 2. Consumption by region × urban/rural ───────────────────────────
hh_cons = hh[["case_id", "region", "reside"]].merge(
    cons[["case_id", "rexpagg",         # real total annual consumption per capita
          "pcrexpagg"]],                 # per-capita real consumption
    on="case_id", how="inner",
)
hh_cons = hh_cons.rename(columns={
    "reside":    "urban_rural",
    "pcrexpagg": "pc_consumption",
})
hh_cons.to_parquet(OUT_DIR / "consumption.parquet", index=False)
print("✓ consumption.parquet saved")

# ── 3. Education attainment by sex (adults 15+) ─────────────────────
roster_edu = roster[["case_id", "PID", "sex", "age"]].merge(
    edu, on=["case_id", "PID"], how="inner"
)
adults = roster_edu.loc[roster_edu["age"] >= 15].copy()
adults = adults.rename(columns={"hh_c09": "edu_level"})

# Simplify education into broad bands
edu_map = {
    "NONE":                          "None",
    "PSLC":                          "Primary",
    "JCE":                           "Junior secondary",
    "MSCE/GCSE":                     "Senior secondary",
    "NON-UNIVERSITY DIPLOMA":        "Post-secondary",
    "UNIVERSITY DIPLOMA":            "University",
    "1ST DEGREE (BSC, BA, ETC.)":    "University",
    "POST-GRADUATE DEGREE (MASTERS, PHD)": "Post-graduate",
}
adults["edu_broad"] = adults["edu_level"].astype(str).str.strip().map(edu_map).fillna("Other")

edu_sex = (
    adults
    .groupby(["edu_broad", "sex"], observed=True)
    .size()
    .reset_index(name="count")
)
# Ordered categories for nice chart ordering
edu_order = ["None", "Primary", "Junior secondary",
             "Senior secondary", "Post-secondary", "University", "Post-graduate", "Other"]
edu_sex["edu_broad"] = pd.Categorical(edu_sex["edu_broad"], categories=edu_order, ordered=True)
edu_sex = edu_sex.sort_values("edu_broad")
edu_sex.to_parquet(OUT_DIR / "edu_by_sex.parquet", index=False)
print("✓ edu_by_sex.parquet saved")

print("\n🎉  All prepared tables saved to", OUT_DIR)