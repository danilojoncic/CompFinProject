import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


def filter_by_year(df, year):
    return df[df["Date"].dt.year == int(year)].set_index("Date")


def calculate_portfolio_metrics(portfolios, df_year, risk_free_rate=0.02):
    results = []

    for name, holdings in portfolios.items():
        tickers = [h["ticker"] for h in holdings]

        close_cols = [f"{t}_Close" for t in tickers if f"{t}_Close" in df_year.columns]
        if not close_cols:
            continue

        prices = df_year[close_cols]
        daily_returns = prices.pct_change().dropna()

        portfolio_returns = daily_returns.mean(axis=1)

        avg_daily_return = portfolio_returns.mean()
        annual_return = avg_daily_return * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)

        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility != 0 else np.nan

        results.append({
            "portfolio": name,
            "annual_return": annual_return,
            "volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio
        })

    return pd.DataFrame(results)

def get_top_portfolios(results_df, top_n=5):
    top_picks = {
        "top_sharpe": results_df.nlargest(top_n, "sharpe_ratio")["portfolio"].tolist(),
        "top_return": results_df.nlargest(top_n, "annual_return")["portfolio"].tolist(),
        "top_low_vol": results_df.nsmallest(top_n, "volatility")["portfolio"].tolist()
    }
    return top_picks

def get_ml_picks(results_df, top_picks, ml_n=5):
    # Combine all top portfolios from existing categories
    top_all = set(top_picks["top_sharpe"]) | set(top_picks["top_return"]) | set(top_picks["top_low_vol"])

    # Select portfolios NOT in top_all
    remaining_df = results_df[~results_df["portfolio"].isin(top_all)]

    # Sort remaining by sharpe_ratio descending (you can choose another metric or composite)
    ml_candidates = remaining_df.sort_values("sharpe_ratio", ascending=False)

    # Pick top ml_n from these as ML picks
    ml_picks = ml_candidates.head(ml_n)["portfolio"].tolist()
    return ml_picks


def plot_portfolios(results_df, year, top_picks, ml_picks):
    plt.figure(figsize=(10, 6))
    plt.scatter(results_df["annual_return"], results_df["sharpe_ratio"],
                alpha=0.3, color="lightgray", label="All Portfolios")

    top5_sharpe = results_df[results_df["portfolio"].isin(top_picks["top_sharpe"])]
    top5_return = results_df[results_df["portfolio"].isin(top_picks["top_return"])]
    top5_low_vol = results_df[results_df["portfolio"].isin(top_picks["top_low_vol"])]
    ml5 = results_df[results_df["portfolio"].isin(ml_picks)]

    plt.scatter(top5_sharpe["annual_return"], top5_sharpe["sharpe_ratio"],
                color="red", s=80, label="Top 5 Sharpe")
    plt.scatter(top5_return["annual_return"], top5_return["sharpe_ratio"],
                color="green", s=80, label="Top 5 Return")
    plt.scatter(top5_low_vol["annual_return"], top5_low_vol["sharpe_ratio"],
                color="blue", s=80, label="Top 5 Lowest Volatility")
    plt.scatter(ml5["annual_return"], ml5["sharpe_ratio"],
                color="purple", s=80, label="Top 5 ML (In-between)")

    plt.xlabel("Annualized Return")
    plt.ylabel("Sharpe Ratio")
    plt.title(f"Portfolios: Return vs Sharpe Ratio ({year})")
    plt.grid(True)
    plt.legend()
    plt.show()


def main(year=2017):
    with open("/Users/danny/PycharmProjects/CompFinProject/datasets/100k_random_portfolios.json", "r") as f:
        portfolios = json.load(f)

    df = pd.read_csv(
        "/Users/danny/PycharmProjects/CompFinProject/datasets/without_nulls_stock_data.csv",
        parse_dates=["Date"]
    )

    df_year = filter_by_year(df, year)
    results_df = calculate_portfolio_metrics(portfolios, df_year)

    top_picks = get_top_portfolios(results_df, top_n=5)
    ml_picks = get_ml_picks(results_df, top_picks, ml_n=5)

    print(f"Top portfolios in {year}:")
    for category, names in top_picks.items():
        print(f"{category}: {names}")
    print(f"ML picks (in-between): {ml_picks}")

    plot_portfolios(results_df, year, top_picks, ml_picks)


if __name__ == "__main__":
    main(2017)
