"""
Telechargement des donnees pour le marche europeen (EURO STOXX 50)
"""
import yfinance as yf
import pandas as pd
from typing import List
import os


def get_eurostoxx50_tickers() -> List[str]:
    """
    Liste des principales actions de l'EURO STOXX 50
    """
    tickers = [
        # France
        'MC.PA', 'OR.PA', 'SAN.PA', 'AIR.PA', 'EL.PA', 'AI.PA', 'BNP.PA', 
        'CS.PA', 'CAP.PA', 'SGO.PA', 'VIV.PA', 'VIE.PA', 'SU.PA', 'ACA.PA',
        # Allemagne
        'SAP.DE', 'SIE.DE', 'ALV.DE', 'DTE.DE', 'MRK.DE', 'BAS.DE', 'BAYN.DE',
        'DPW.DE', 'ENR.DE', 'RWE.DE', 'HEI.DE', 'IFX.DE', 'LIN.DE', 'MTX.DE',
        # Pays-Bas
        'ASML.AS', 'UNA.AS', 'ING.AS', 'DSM.AS', 'AD.AS', 'ASRNL.AS', 'REN.AS',
        # Espagne
        'ITX.MC', 'SAN.MC', 'BBVA.MC', 'TEF.MC', 'REP.MC', 'AENA.MC', 'COL.MC',
        # Italie
        'ENEL.MI', 'ENI.MI', 'ISP.MI', 'UCG.MI', 'G.MI', 'TEN.MI', 'SRG.MI',
        # Suisse
        'NESN.SW', 'NOVN.SW', 'ROG.SW', 'ZURN.SW', 'ABBN.SW', 'UBSG.SW', 'SCMN.SW',
        # Autres
        'ORNB.VI', 'VER.VI', 'FLTR.IR', 'CRH.IR', 'BIRG.IR', 'ALC', 'STLA'
    ]
    return tickers


def get_extended_period_data(tickers: List[str], 
                              start_date: str = '2005-01-01',
                              end_date: str = '2024-12-31',
                              cache_file: str = 'data/european_prices.csv') -> pd.DataFrame:
    """
    Telecharge les donnees historiques pour une longue periode incluant les crises
    """
    
    if os.path.exists(cache_file):
        print(f"Chargement depuis le cache: {cache_file}")
        return pd.read_csv(cache_file, index_col=0, parse_dates=True)
    
    print(f"Telechargement des donnees europeennes pour {len(tickers)} actions...")
    print(f"Periode: {start_date} a {end_date}")
    print("Cette periode inclut:")
    print("  - 2007-2009: Crise financiere")
    print("  - 2010-2012: Crise de la dette europeenne")
    print("  - 2020: COVID-19")
    print("  - 2022: Inflation/montee des taux")
    
    all_data = []
    valid_tickers = []
    
    for i, ticker in enumerate(tickers):
        if (i + 1) % 10 == 0:
            print(f"  Progression: {i + 1}/{len(tickers)}")
        
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if len(data) > 500:  # Au moins 2 ans de donnees
                all_data.append(data['Close'].rename(ticker))
                valid_tickers.append(ticker)
                print(f"    [OK] {ticker}: {len(data)} jours")
            else:
                print(f"    [SKIP] {ticker}: trop peu de donnees ({len(data)} jours)")
        except Exception as e:
            print(f"    [ERR] {ticker}: {str(e)[:50]}")
    
    if len(all_data) == 0:
        raise ValueError("Aucune donnee telechargee")
    
    # Combiner toutes les donnees
    prices = pd.concat(all_data, axis=1)
    prices = prices.dropna(axis=1, thresh=len(prices) * 0.5)  # Garder colonnes avec >50% de donnees
    prices = prices.ffill().bfill()  # Remplir valeurs manquantes
    
    print(f"\nDonnees telechargees: {prices.shape[0]} jours, {prices.shape[1]} actions")
    print(f"Periode couverte: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    
    # Sauvegarder
    prices.to_csv(cache_file)
    print(f"Donnees sauvegardees: {cache_file}")
    
    return prices


def analyze_periods(prices: pd.DataFrame):
    """
    Analyse les differentes periodes historiques
    """
    periods = {
        'Bulle Internet': ('2000-01-01', '2002-12-31'),
        'Pre-Crise': ('2003-01-01', '2007-06-30'),
        'Crise Financiere': ('2007-07-01', '2009-06-30'),
        'Reprise': ('2009-07-01', '2011-12-31'),
        'Crise Dette Europe': ('2012-01-01', '2012-12-31'),
        'Bull Market': ('2013-01-01', '2019-12-31'),
        'COVID-19': ('2020-01-01', '2020-12-31'),
        'Post-COVID': ('2021-01-01', '2021-12-31'),
        'Inflation/Taux': ('2022-01-01', '2024-12-31')
    }
    
    print("\n" + "="*70)
    print("ANALYSE DES PERIODES HISTORIQUES")
    print("="*70)
    
    results = []
    for period_name, (start, end) in periods.items():
        period_data = prices.loc[start:end]
        if len(period_data) > 0:
            # Calculer le rendement du marche (moyenne de toutes les actions)
            market_returns = period_data.pct_change().mean(axis=1)
            total_return = (1 + market_returns).cumprod().iloc[-1] - 1
            
            # Volatilite
            volatility = market_returns.std() * np.sqrt(252) * 100
            
            # Max drawdown
            cum = (1 + market_returns).cumprod()
            running_max = cum.cummax()
            drawdown = (cum - running_max) / running_max
            max_dd = drawdown.min() * 100
            
            results.append({
                'Periode': period_name,
                'Start': start,
                'End': end,
                'Rendement (%)': total_return * 100,
                'Volatilite (%)': volatility,
                'Max DD (%)': max_dd,
                'Jours': len(period_data)
            })
            
            print(f"\n{period_name} ({start} a {end}):")
            print(f"  Rendement: {total_return*100:+.1f}%")
            print(f"  Volatilite: {volatility:.1f}%")
            print(f"  Max Drawdown: {max_dd:.1f}%")
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    import numpy as np
    
    tickers = get_eurostoxx50_tickers()
    prices = get_extended_period_data(
        tickers,
        start_date='2000-01-01',
        end_date='2024-12-31',
        cache_file='data/european_prices_extended.csv'
    )
    
    # Analyser les periodes
    period_analysis = analyze_periods(prices)
    period_analysis.to_csv('data/period_analysis_europe.csv', index=False)
    
    print("\n" + "="*70)
    print("RESUME GLOBAL")
    print("="*70)
    print(f"Periode totale: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Nombre d'actions: {prices.shape[1]}")
    print(f"Nombre de jours: {prices.shape[0]}")
    
    # Rendement total sur toute la periode
    all_returns = prices.pct_change().mean(axis=1)
    total_perf = (1 + all_returns).cumprod().iloc[-1] - 1
    print(f"\nRendement total du marche europeen: {total_perf*100:.1f}%")
    print(f"Rendement annualise: {((1+total_perf)**(1/24.5)-1)*100:.1f}%")
