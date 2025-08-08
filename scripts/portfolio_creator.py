import json
import random

with open("/Users/danny/PycharmProjects/CompFinProject/datasets/ticker_for_portfolio.json", "r") as f:
    ticker_name_map = json.load(f)

tickers = list(ticker_name_map.keys())

num_portfolios = 100000
portfolios = {}

for i in range(1, num_portfolios + 1):
    size = random.randint(2, 10)
    selected_tickers = random.sample(tickers, size)

    portfolio_name = f"portfolio{i}"
    portfolios[portfolio_name] = [
        {"ticker": t, "name": ticker_name_map[t]} for t in selected_tickers
    ]

output_path = "../datasets/100k_random_portfolios.json"
with open(output_path, "w") as f:
    json.dump(portfolios, f, indent=4)

print(f"Saved {num_portfolios} named portfolios to: {output_path}")
