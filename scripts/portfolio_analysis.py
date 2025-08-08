import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def filterByYear(df,year):
    return df[(df["Date"].dt.year == year)].set_index("Date")


def main():
    # === 1. Load portfolios ===
    with open("/Users/danny/PycharmProjects/CompFinProject/datasets/100k_random_portfolios.json", "r") as f:
        portfolios = json.load(f)

    # === 2. Load stock price data ===
    df = pd.read_csv("/Users/danny/PycharmProjects/CompFinProject/datasets/without_nulls_stock_data.csv",
                     parse_dates=["Date"])
    print("")

    df_2017 = filterByYear(df, "2017")

    # === 4. Calculate metrics for each portfolio ===
    results = []

    risk_free_rate = 0.02  # Example: 2% annualized

    for name, holdings in portfolios.items():
        tickers = [h["ticker"] for h in holdings]

        # Get closing prices for the tickers
        close_cols = [f"{t}_Close" for t in tickers if f"{t}_Close" in df_2017.columns]
        if not close_cols:  # Skip portfolios with missing data
            continue

        prices = df_2017[close_cols]
        daily_returns = prices.pct_change().dropna()

        # Equal-weight portfolio
        portfolio_returns = daily_returns.mean(axis=1)

        # Annualized return & volatility
        avg_daily_return = portfolio_returns.mean()
        annual_return = avg_daily_return * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)

        # Sharpe ratio
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility != 0 else np.nan

        results.append({
            "portfolio": name,
            "annual_return": annual_return,
            "volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio
        })

    # === 5. Convert results to DataFrame ===
    results_df = pd.DataFrame(results)

    # === 6. Find top 5 by each metric ===
    top5_return = results_df.nlargest(5, "annual_return")
    top5_volatility = results_df.nsmallest(5, "volatility")
    top5_sharpe = results_df.nlargest(5, "sharpe_ratio")

    plt.figure(figsize=(10, 6))
    plt.scatter(results_df["annual_return"], results_df["sharpe_ratio"],
                alpha=0.3, color="lightgray", label="All Portfolios")

    top5_sharpe = results_df.nlargest(5, "sharpe_ratio")
    top5_return = results_df.nlargest(5, "annual_return")
    top5_low_vol = results_df.nsmallest(5, "volatility")

    plt.scatter(top5_sharpe["annual_return"], top5_sharpe["sharpe_ratio"],
                color="red", s=80, label="Top 5 Sharpe")
    plt.scatter(top5_return["annual_return"], top5_return["sharpe_ratio"],
                color="green", s=80, label="Top 5 Return")
    plt.scatter(top5_low_vol["annual_return"], top5_low_vol["sharpe_ratio"],
                color="blue", s=80, label="Top 5 Lowest Volatility")

    plt.xlabel("Annualized Return")
    plt.ylabel("Sharpe Ratio")
    plt.title("Portfolios: Return vs Sharpe Ratio (2017)")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
