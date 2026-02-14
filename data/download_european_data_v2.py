"""
Telechargement des donnees pour le marche europeen - Version 2
Gestion amelioree des donnees manquantes entre differents marches
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List
import os


def get_european_tickers() -> List[str]:
    """
    Liste des principales actions europeennes (EURO STOXX 50 + supplementaires)
    """
    tickers = [
        # France - CAC 40
        'MC.PA', 'OR.PA', 'SAN.PA', 'AIR.PA', 'EL.PA', 'AI.PA', 'BNP.PA', 
        'CS.PA', 'CAP.PA', 'SGO.PA', 'VIV.PA', 'VIE.PA', 'SU.PA', 'ACA.PA',
        # Allemagne - DAX
        'SAP.DE', 'SIE.DE', 'ALV.DE', 'DTE.DE', 'MRK.DE', 'BAS.DE', 'BAYN.DE',
        'RWE.DE', 'HEI.DE', 'IFX.DE', 'LIN.DE', 'MTX.DE', 'SHL.DE', 'SY1.DE',
        # Pays-Bas
        'ASML.AS', 'REN.AS', 'AD.AS', 'ASRNL.AS',
        # Espagne - IBEX 35
        'ITX.MC', 'SAN.MC', 'BBVA.MC', 'TEF.MC', 'REP.MC', 'AENA.MC', 'COL.MC',
        # Italie - FTSE MIB
        'ENEL.MI', 'ENI.MI', 'ISP.MI', 'UCG.MI', 'G.MI', 'TEN.MI', 'SRG.MI',
        # Suisse (non-EU mais important)
        'NESN.SW', 'NOVN.SW', 'ROG.SW', 'ZURN.SW', 'ABBN.SW', 'UBSG.SW', 'SCMN.SW',
        # Autres
        'VER.VI', 'BIRG.IR', 'STLA'
    ]
    return tickers


def download_european_data(start_date='2005-01-01', 
                           end_date='2024-12-31',
                           min_days=500):
    """
    Telecharge les donnees europeennes avec gestion intelligente des NaN
    """
    cache_file = 'data/european_prices_clean.csv'
    
    if os.path.exists(cache_file):
        print(f"Chargement depuis le cache: {cache_file}")
        return pd.read_csv(cache_file, index_col=0, parse_dates=True)
    
    tickers = get_european_tickers()
    print(f"Telechargement de {len(tickers)} actions europeennes...")
    print(f"Periode: {start_date} a {end_date}")
    
    all_data = {}
    
    for i, ticker in enumerate(tickers):
        if (i + 1) % 5 == 0:
            print(f"  {i+1}/{len(tickers)}...", end='\r')
        
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date, auto_adjust=True)
            
            if len(data) >= min_days:
                all_data[ticker] = data['Close']
                
        except Exception as e:
            continue
    
    print(f"\n{len(all_data)} actions telechargees avec succes")
    
    if len(all_data) == 0:
        raise ValueError("Aucune donnee telechargee")
    
    # Creer le DataFrame
    prices = pd.DataFrame(all_data)
    print(f"Shape initial: {prices.shape}")
    
    # Strategie de gestion des NaN:
    # 1. Remplir les trous avec la derniere valeur connue (forward fill)
    # 2. Puis backward fill pour les valeurs au debut
    # 3. Supprimer les colonnes qui ont encore trop de NaN (>30%)
    
    prices = prices.ffill(limit=5)  # Max 5 jours consecutifs
    prices = prices.bfill(limit=5)
    
    # Supprimer les colonnes avec >30% de NaN
    nan_ratio = prices.isna().sum() / len(prices)
    valid_cols = nan_ratio[nan_ratio < 0.3].index
    prices = prices[valid_cols]
    
    print(f"Shape apres nettoyage: {prices.shape}")
    print(f"Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    
    # Remplir les NaN restants par interpolation
    prices = prices.interpolate(method='linear', limit=3)
    prices = prices.dropna()  # Supprimer les lignes avec encore des NaN
    
    print(f"Shape final: {prices.shape}")
    
    # Sauvegarder
    prices.to_csv(cache_file)
    print(f"Donnees sauvegardees: {cache_file}")
    
    return prices


if __name__ == "__main__":
    prices = download_european_data(
        start_date='2005-01-01',
        end_date='2024-12-31'
    )
    
    print("\nApercu des donnees:")
    print(prices.head())
    print("\nActions disponibles:")
    print(prices.columns.tolist())
