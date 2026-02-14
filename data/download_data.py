"""
Telechargement des donnees historiques d'actions
"""
import yfinance as yf
import pandas as pd
from typing import List
import os


def get_sp500_tickers(n: int = 100) -> List[str]:
    """
    Recupere les tickers du S&P 500 (les N premieres capitalisations)
    """
    # Liste des tickers principaux du S&P 500
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'UNH', 'JNJ', 'JPM',
        'V', 'PG', 'MA', 'HD', 'CVX', 'MRK', 'LLY', 'PEP', 'KO', 'ABBV',
        'BAC', 'AVGO', 'TMO', 'COST', 'DIS', 'PFE', 'ABT', 'ACN', 'WMT', 'MCD',
        'ADBE', 'CSCO', 'VZ', 'NKE', 'TXN', 'CMCSA', 'CRM', 'DHR', 'BMY', 'NEE',
        'PM', 'RTX', 'HON', 'LIN', 'UNP', 'IBM', 'LOW', 'UPS', 'QCOM', 'AMGN',
        'SPGI', 'CAT', 'MS', 'GS', 'BLK', 'INTU', 'PLD', 'DE', 'MDT', 'AXP',
        'LMT', 'AMAT', 'BKNG', 'TJX', 'CI', 'GILD', 'ADI', 'C', 'SBUX', 'MMC',
        'VRTX', 'ISRG', 'MDLZ', 'SYK', 'ADP', 'REGN', 'ZTS', 'SO', 'BSX', 'ELV',
        'TMUS', 'LRCX', 'EOG', 'FIS', 'ETN', 'ITW', 'SLB', 'CME', 'BDX', 'TGT',
        'AON', 'CL', 'MU', 'CSX', 'WM', 'FCX', 'NOC', 'HUM', 'PYPL', 'AMT'
    ]
    return tickers[:n]


def download_stock_data(tickers: List[str], 
                       start_date: str = '2018-01-01',
                       end_date: str = '2024-12-31',
                       cache_dir: str = 'data') -> pd.DataFrame:
    """
    Telecharge les donnees de prix pour une liste de tickers
    """
    cache_file = os.path.join(cache_dir, 'stock_prices.csv')
    
    # Verifier si les donnees sont en cache
    if os.path.exists(cache_file):
        print(f"Chargement des donnees depuis le cache: {cache_file}")
        return pd.read_csv(cache_file, index_col=0, parse_dates=True)
    
    print(f"Telechargement des donnees pour {len(tickers)} actions...")
    print(f"Periode: {start_date} a {end_date}")
    
    all_data = []
    valid_tickers = []
    
    for i, ticker in enumerate(tickers):
        if (i + 1) % 10 == 0:
            print(f"  Progression: {i + 1}/{len(tickers)}")
        
        try:
            # Utiliser yf.Ticker pour chaque action
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if len(data) > 100:  # Verifier qu'on a assez de donnees
                all_data.append(data['Close'].rename(ticker))
                valid_tickers.append(ticker)
        except Exception as e:
            print(f"  Erreur pour {ticker}: {e}")
    
    if len(all_data) == 0:
        raise ValueError("Aucune donnee telechargee. Verifiez votre connexion internet.")
    
    # Combiner toutes les donnees
    prices = pd.concat(all_data, axis=1)
    prices = prices.dropna(axis=1, thresh=len(prices) * 0.8)  # Garder les colonnes avec >80% de donnees
    prices = prices.ffill()  # Remplir les valeurs manquantes (forward fill)
    prices = prices.bfill()  # Backward fill pour les valeurs au debut
    
    print(f"\nDonnees telechargees: {prices.shape[0]} jours, {prices.shape[1]} actions")
    
    # Sauvegarder en cache
    prices.to_csv(cache_file)
    print(f"Donnees sauvegardees dans: {cache_file}")
    
    return prices


if __name__ == "__main__":
    # Telecharger les donnees du S&P 500 (top 100)
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    print(f"\nApercu des donnees:")
    print(prices.head())
