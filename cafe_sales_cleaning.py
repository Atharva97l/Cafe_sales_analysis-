
import pandas as pd
import numpy as np

# load data
df = pd.read_csv("dirty_cafe_sales.csv")
df_clean = df.copy()

# ----------------------------
# TEXT CLEANING
# ----------------------------
text_cols = ["Payment Method", "Location", "Transaction Date"]

df_clean[text_cols] = (
    df_clean[text_cols]
    .replace("ERROR", "UNKNOWN")
    .fillna("UNKNOWN")
)

# clean transaction id
df_clean["Transaction ID"] = (
    df_clean["Transaction ID"]
    .astype(str)
    .str.replace("TXN_", "", regex=False)
)

# ----------------------------
# NUMERIC CLEANING
# ----------------------------
num_cols = ["Quantity", "Price Per Unit", "Total Spent"]

df_clean[num_cols] = (
    df_clean[num_cols]
    .replace("error", np.nan)
    .apply(pd.to_numeric, errors="coerce")
)

# ----------------------------
# FIX MISSING VALUES LOGICALLY
# ----------------------------

# fill Quantity if missing
mask_qty_nan = (
    df_clean["Quantity"].isna() &
    df_clean["Price Per Unit"].notna() &
    df_clean["Total Spent"].notna()
)

df_clean.loc[mask_qty_nan, "Quantity"] = (
    df_clean.loc[mask_qty_nan, "Total Spent"] /
    df_clean.loc[mask_qty_nan, "Price Per Unit"]
)

# fill Price Per Unit if missing
mask_ppu_nan = (
    df_clean["Price Per Unit"].isna() &
    df_clean["Quantity"].notna() &
    df_clean["Total Spent"].notna()
)

df_clean.loc[mask_ppu_nan, "Price Per Unit"] = (
    df_clean.loc[mask_ppu_nan, "Total Spent"] /
    df_clean.loc[mask_ppu_nan, "Quantity"]
)

# 🔴 FIX HERE: fill Total Spent if missing
mask_ts_nan = (
    df_clean["Total Spent"].isna() &
    df_clean["Quantity"].notna() &
    df_clean["Price Per Unit"].notna()
)

df_clean.loc[mask_ts_nan, "Total Spent"] = (
    df_clean.loc[mask_ts_nan, "Quantity"] *
    df_clean.loc[mask_ts_nan, "Price Per Unit"]
)

# ----------------------------
# STANDARDIZE COLUMN NAMES
# ----------------------------
df_clean = df_clean.rename(columns={
    "Price Per Unit": "PricePerUnit",
    "Total Spent": "TotalSpent"
})

# ----------------------------
# SAVE OUTPUT
# ----------------------------
df_clean.to_excel("cafe_data.xlsx", index=False)

