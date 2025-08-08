import pandas as pd
import yfinance as yf
import json


df_original = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/stock_data_master_20150811_20250808.csv")
df_cleaned = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/without_nulls_stock_data.csv")

print(df_cleaned.head())
print(df_original.head())

original_cols = set(df_original.columns)
cleaned_cols = set(df_cleaned.columns)

deleted_cols = original_cols - cleaned_cols

print("Deleted columns (those that had nulls):")
print(sorted(deleted_cols))

deleted_tickers = {col.split('_')[0] for col in deleted_cols}

print("Tickers that had columns with nulls (i.e., deleted):")
print(sorted(deleted_tickers))

sugary_df = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/stock_summary_20150811_20250808.csv")

filtered_sugary_df = sugary_df[~sugary_df['Ime'].isin(deleted_tickers)]

filtered_sugary_df.to_csv("clean_output.csv", index=False)
print("Filtered summary saved.")


tickers = sorted(filtered_sugary_df["Ime"].tolist())
ticker_company = {}
for ticker in tickers:
    try:
        info = yf.Ticker(ticker).info
        ticker_company[ticker] = info.get("shortName", "Unknown")
    except:
        ticker_company[ticker] = "Unknown"

# Save to JSON
with open("../datasets/ticker_for_portfolio.json", "w") as f:
    json.dump(ticker_company, f, indent=4)

print("Tickers with names saved.")



