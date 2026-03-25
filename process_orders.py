"""
process_orders.py
-----------------
E-Commerce Order Data Processing Pipeline
Author : Muathaf
Purpose: Load raw Shopify order exports, clean the data,
         calculate revenue metrics, and export a daily report.

This script demonstrates:
  - Real-world data cleaning with pandas
  - Handling missing values and filtering bad records
  - Calculated columns and aggregation
  - Professional terminal output and CSV export
"""

import pandas as pd


# ─────────────────────────────────────────
# 1. LOAD RAW DATA
# ─────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load the CSV file into a pandas DataFrame."""
    print(f"\n📂  Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"    {len(df)} rows loaded.\n")
    return df


# ─────────────────────────────────────────
# 2. CLEAN DATA
# ─────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw order data:
      - Drop rows where CustomerName is missing (can't process anonymous orders)
      - Remove Cancelled orders (not counted as revenue)
      - Strip extra whitespace from string columns
    """
    initial_count = len(df)

    # Strip whitespace from all string columns
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Drop rows with missing CustomerName
    df = df.dropna(subset=["CustomerName"])
    missing_dropped = initial_count - len(df)
    if missing_dropped:
        print(f"🗑️   Dropped {missing_dropped} row(s) with missing CustomerName.")

    # Filter out Cancelled orders
    cancelled_count = (df["Status"] == "Cancelled").sum()
    df = df[df["Status"] != "Cancelled"]
    if cancelled_count:
        print(f"🚫  Removed {cancelled_count} Cancelled order(s).")

    print(f"✅  {len(df)} clean rows remaining.\n")
    return df


# ─────────────────────────────────────────
# 3. CALCULATE METRICS
# ─────────────────────────────────────────

def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Total_Value column: Quantity × Price.
    This represents the revenue per order line.
    """
    df = df.copy()
    df["Total_Value"] = df["Quantity"] * df["Price"]
    df["Total_Value"] = df["Total_Value"].round(2)
    return df


# ─────────────────────────────────────────
# 4. PRINT SUMMARY REPORT
# ─────────────────────────────────────────

def print_summary(df: pd.DataFrame) -> None:
    """Print a clean summary of key business metrics to the terminal."""
    total_revenue    = df["Total_Value"].sum()
    successful_orders = len(df[df["Status"] == "Completed"])
    avg_order_value  = df["Total_Value"].mean()
    top_item         = df.groupby("Item")["Total_Value"].sum().idxmax()

    print("=" * 45)
    print("        DAILY ORDER REPORT — SUMMARY")
    print("=" * 45)
    print(f"  Total Orders Processed : {len(df)}")
    print(f"  Successful (Completed) : {successful_orders}")
    print(f"  Total Revenue          : ${total_revenue:,.2f}")
    print(f"  Average Order Value    : ${avg_order_value:,.2f}")
    print(f"  Top Revenue Item       : {top_item}")
    print("=" * 45)
    print()


# ─────────────────────────────────────────
# 5. EXPORT CLEAN REPORT
# ─────────────────────────────────────────

def export_report(df: pd.DataFrame, output_path: str) -> None:
    """Export the cleaned and enriched DataFrame to a CSV report."""
    df.to_csv(output_path, index=False)
    print(f"📄  Report exported to: {output_path}")


# ─────────────────────────────────────────
# MAIN — run the full pipeline
# ─────────────────────────────────────────

if __name__ == "__main__":

    # File paths — change these if needed
    INPUT_FILE  = "shopify_orders.csv"
    OUTPUT_FILE = "daily_report.csv"

    # Run the pipeline step by step
    raw_df   = load_data(INPUT_FILE)
    clean_df = clean_data(raw_df)
    final_df = calculate_metrics(clean_df)

    print_summary(final_df)
    export_report(final_df, OUTPUT_FILE)

    print("\n✔   Pipeline complete.\n")
