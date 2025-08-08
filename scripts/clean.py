import pandas as pd

def drop_tickers_with_nans(name):
    df = pd.read_csv(name)
    tickers = set(col.split('_')[0] for col in df.columns)
    tickers_to_drop = []
    for ticker in tickers:
        ticker_cols = [col for col in df.columns if col.startswith(ticker + '_')]
        if df[ticker_cols].isnull().values.any():
            tickers_to_drop.extend(ticker_cols)

    df_cleaned = df.drop(columns=tickers_to_drop)

    return df_cleaned

def main():
    df_clean = drop_tickers_with_nans("/Users/danny/PycharmProjects/CompFinProject/datasets/stock_data_master_20150811_20250808.csv")
    df_clean.to_csv("without_nulls_stock_data.csv", index=False)

if __name__ == "__main__":
    main()
