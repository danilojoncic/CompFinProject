import pandas as pd



df_original = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/stock_data_master_20150811_20250808.csv")
df_cleaned = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/without_nulls_stock_data.csv")


print(df_cleaned.head())
print(df_original.head())

original_cols = set(df_original.columns)
cleaned_cols = set(df_cleaned.columns)

# Find which columns were removed
deleted_cols = original_cols - cleaned_cols

print("Deleted columns (those that had nulls):")
print(sorted(deleted_cols))

deleted_tickers = {col.split('_')[0] for col in deleted_cols}

print("Tickers that had columns with nulls (i.e., deleted):")
print(sorted(deleted_tickers))