import ssl
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')


def download_stock_data(tickers, start_date, end_date):
    print(f"Preuzimanje podataka za {len(tickers)} akcija...")
    print(f"Period: {start_date.strftime('%Y-%m-%d')} do {end_date.strftime('%Y-%m-%d')}")

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        progress=False,
        group_by='ticker',
        threads=True
    )

    # Organizovanje podataka
    stock_data = {}

    if len(tickers) == 1:
        # Ako je samo jedan ticker
        ticker = tickers[0]
        stock_data[ticker] = {
            'Open': data['Open'],
            'High': data['High'],
            'Low': data['Low'],
            'Close': data['Close'],
            'Volume': data['Volume']
        }
    else:
        # Više tickera
        for ticker in tqdm(tickers, desc="Organizovanje podataka"):
            try:
                stock_data[ticker] = {
                    'Open': data[ticker]['Open'],
                    'High': data[ticker]['High'],
                    'Low': data[ticker]['Low'],
                    'Close': data[ticker]['Close'],
                    'Volume': data[ticker]['Volume']
                }
            except KeyError:
                print(f"Upozorenje: Nema podataka za {ticker}")
                continue

    return stock_data


def create_master_dataset(stock_data):
    """Kreira glavni dataset sa svim dnevnim podacima"""
    all_dataframes = []

    for ticker, ticker_data in stock_data.items():
        # Kreiranje DataFrame-a za ticker
        df = pd.DataFrame(ticker_data)

        # Dodavanje prefiksa ticker-a u nazive kolona
        df.columns = [f'{ticker}_{col}' for col in df.columns]

        all_dataframes.append(df)

    # Kombinovanje svih DataFrame-a
    master_df = pd.concat(all_dataframes, axis=1)

    # Uklanjanje redova gde su svi podaci NaN
    master_df = master_df.dropna(how='all')

    return master_df


def calculate_basic_returns(master_df, tickers):
    """Izračunava osnovne dnevne prinose"""
    returns_df = pd.DataFrame()

    for ticker in tickers:
        close_col = f'{ticker}_Close'
        if close_col in master_df.columns:
            returns_df[f'{ticker}_Daily_Return'] = master_df[close_col].pct_change()

    return returns_df


def get_data_summary(master_df, tickers):
    """Daje kratak pregled podataka"""
    summary = {}

    for ticker in tickers:
        close_col = f'{ticker}_Close'
        volume_col = f'{ticker}_Volume'

        if close_col in master_df.columns:
            close_prices = master_df[close_col].dropna()
            volumes = master_df[volume_col].dropna()

            summary[ticker] = {
                'Početna_Cena': round(close_prices.iloc[0], 2),
                'Poslednja_Cena': round(close_prices.iloc[-1], 2),
                'Min_Cena': round(close_prices.min(), 2),
                'Max_Cena': round(close_prices.max(), 2),
                'Prosečna_Cena': round(close_prices.mean(), 2),
                'Prosečan_Volume': int(volumes.mean()),
                'Broj_Dana_Sa_Podacima': len(close_prices),
                'Ukupna_Promena_%': round(((close_prices.iloc[-1] / close_prices.iloc[0]) - 1) * 100, 2)
            }

    return pd.DataFrame(summary).T

def get_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    ssl._create_default_https_context = ssl._create_unverified_context  # Bypass SSL
    try:
        tables = pd.read_html(url)
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        # Fix tickers with '.' to match actual ticker convention (e.g., BRK.B → BRK-B)
        tickers = [ticker.replace('.', '-') for ticker in tickers]
        print(tickers)
        return tickers
    except Exception as e:
        print(f"Error retrieving S&P 500 tickers: {e}")
        return []


def main():
    tickers = get_tickers()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10 * 365)

    print("=" * 50)
    print("PREUZIMANJE OSNOVNIH STOCK PODATAKA")
    print("=" * 50)
    stock_data = download_stock_data(tickers, start_date, end_date)

    print("\nKreiranje master dataset-a...")
    master_df = create_master_dataset(stock_data)

    print("Izračunavanje dnevnih prinosa...")
    returns_df = calculate_basic_returns(master_df, tickers)

    print("Kreiranje pregleda podataka...")
    summary_df = get_data_summary(master_df, tickers)

    print("\n" + "=" * 50)
    print("PREGLED PODATAKA")
    print("=" * 50)
    print(f"Ukupno dana sa podacima: {len(master_df)}")
    print(f"Ukupno kolona: {len(master_df.columns)}")
    print(f"Period: {master_df.index[0].strftime('%Y-%m-%d')} do {master_df.index[-1].strftime('%Y-%m-%d')}")

    print("\nSUMMARY PO AKCIJAMA:")
    print(summary_df.to_string())

    print(f"\nPrimer podataka (zadnjih 5 dana):")
    # Prikaz samo Close cena za lakše čitanje
    close_columns = [col for col in master_df.columns if 'Close' in col]
    print(master_df[close_columns].tail().to_string())

    # 6. Čuvanje podataka
    print("\n" + "=" * 50)
    print("ČUVANJE PODATAKA")
    print("=" * 50)

    # Master dataset sa svim podacima
    master_filename = f"stock_data_master_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
    master_df.to_csv(master_filename)
    print(f"✓ Master dataset sačuvan: {master_filename}")

    returns_filename = f"daily_returns_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
    returns_df.to_csv(returns_filename)
    print(f"✓ Dnevni prinosi sačuvani: {returns_filename}")

    summary_filename = f"stock_summary_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
    summary_df.to_csv(summary_filename)
    print(f"✓ Summary sačuvan: {summary_filename}")

    print("\nKreiranje pojednostavljenih CSV fajlova...")

    close_prices = master_df[[col for col in master_df.columns if 'Close' in col]].copy()
    close_prices.columns = [col.replace('_Close', '') for col in close_prices.columns]
    close_prices.to_csv('close_prices_simple.csv')
    print("✓ Close cene sačuvane: close_prices_simple.csv")

    volumes = master_df[[col for col in master_df.columns if 'Volume' in col]].copy()
    volumes.columns = [col.replace('_Volume', '') for col in volumes.columns]
    volumes.to_csv('volumes_simple.csv')
    print("✓ Volume podaci sačuvani: volumes_simple.csv")

    print("\n" + "=" * 50)
    print("GOTOVO!")
    print("=" * 50)
    print("Sada imate osnovne podatke i možete ih koristiti za bilo kakve analize.")
    print("Glavni fajlovi:")
    print(f"• {master_filename} - kompletan dataset")
    print(f"• close_prices_simple.csv - samo cene (lakše za učitavanje)")
    print(f"• daily_returns_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv - dnevni prinosi")

    return master_df, returns_df, summary_df


if __name__ == "__main__":
    master_df, returns_df, summary_df = main()