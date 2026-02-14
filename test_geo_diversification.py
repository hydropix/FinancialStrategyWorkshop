#!/usr/bin/env python3
"""
Test de stratégies de diversification géographique
Comparaison de différentes allocations régionales
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from data.download_data import download_stock_data


# ETF représentatifs par région (tickers Yahoo Finance)
GEO_ETF = {
    # US
    'SPY': {'name': 'S&P 500', 'region': 'US', 'type': 'Developed'},
    'VEA': {'name': 'Developed Markets ex-US', 'region': 'Developed ex-US', 'type': 'Developed'},
    'IEFA': {'name': 'MSCI EAFE', 'region': 'EAFE', 'type': 'Developed'},
    'EEM': {'name': 'MSCI Emerging Markets', 'region': 'EM', 'type': 'Emerging'},
    'VWO': {'name': 'FTSE Emerging Markets', 'region': 'EM', 'type': 'Emerging'},
    'IEV': {'name': 'S&P Europe 350', 'region': 'Europe', 'type': 'Developed'},
    'EWJ': {'name': 'MSCI Japan', 'region': 'Japan', 'type': 'Developed'},
    'EPP': {'name': 'MSCI Pacific ex-Japan', 'region': 'Pacific ex-JP', 'type': 'Developed'},
    'ACWI': {'name': 'MSCI All Country World', 'region': 'World', 'type': 'All'},
    'VT': {'name': 'Total World Stock', 'region': 'World', 'type': 'All'},
}


def load_geo_data(start_date='2010-01-01', end_date='2024-12-31'):
    """
    Télécharge les données des ETF géographiques
    """
    print("="*70)
    print("CHARGEMENT DES DONNÉES GÉOGRAPHIQUES")
    print("="*70)
    
    tickers = list(GEO_ETF.keys())
    print(f"\nTéléchargement de {len(tickers)} ETF régionaux...")
    for ticker, info in GEO_ETF.items():
        print(f"  - {ticker}: {info['name']} ({info['region']})")
    
    # Force new download by using a different cache file
    import yfinance as yf
    print("\n[Téléchargement Yahoo Finance...]")
    
    all_data = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
            if not data.empty:
                # Handle multi-index columns from yfinance
                if isinstance(data.columns, pd.MultiIndex):
                    close_col = ('Close', ticker)
                    if close_col in data.columns:
                        all_data[ticker] = data[close_col]
                        print(f"  [OK] {ticker}: {len(data)} jours")
                elif 'Close' in data.columns:
                    all_data[ticker] = data['Close']
                    print(f"  [OK] {ticker}: {len(data)} jours")
        except Exception as e:
            print(f"  [ERR] {ticker}: {e}")
    
    if not all_data:
        print("[!] Aucune donnée téléchargée")
        return pd.DataFrame()
    
    prices = pd.DataFrame(all_data)
    prices = prices.dropna(axis=1, how='all')  # Remove empty columns
    prices = prices.ffill()  # Forward fill
    
    # Vérifier la disponibilité des données
    available = prices.columns.tolist()
    missing = [t for t in tickers if t not in available]
    
    if missing:
        print(f"\n[!] ETF non disponibles: {missing}")
    
    print(f"\n[OK] Données chargées: {prices.index[0].date()} à {prices.index[-1].date()}")
    print(f"     {len(available)} ETF disponibles, {len(prices)} jours de données")
    
    return prices


def calculate_metrics(returns, freq=252):
    """Calcule les métriques de performance"""
    total_return = (1 + returns).prod() - 1
    annualized_return = (1 + total_return) ** (freq / len(returns)) - 1
    volatility = returns.std() * np.sqrt(freq)
    sharpe = annualized_return / volatility if volatility > 0 else 0
    
    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    cummax = cumulative.cummax()
    drawdown = (cumulative - cummax) / cummax
    max_dd = drawdown.min()
    
    return {
        'total_return': total_return * 100,
        'annualized_return': annualized_return * 100,
        'volatility': volatility * 100,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd * 100
    }


def strategy_buy_hold(prices, weights, name="Buy & Hold"):
    """
    Stratégie Buy & Hold avec poids fixes
    """
    returns = prices.pct_change().dropna()
    
    # Calculer les rendements du portefeuille
    portfolio_returns = pd.Series(0, index=returns.index)
    for ticker, weight in weights.items():
        if ticker in returns.columns:
            portfolio_returns += returns[ticker] * weight
    
    metrics = calculate_metrics(portfolio_returns)
    metrics['name'] = name
    metrics['weights'] = weights
    
    return metrics, portfolio_returns


def strategy_momentum_rotation(prices, lookback_months=12, top_n=2, rebalance_freq='Q'):
    """
    Stratégie de rotation par momentum géographique
    Sélectionne les top_n ETF avec le meilleur momentum
    """
    lookback_days = lookback_months * 21
    returns = prices.pct_change().dropna()
    
    # Déterminer les dates de rebalancement
    if rebalance_freq == 'Q':
        rebalance_dates = pd.date_range(start=returns.index[0], end=returns.index[-1], freq='QS')
    else:
        rebalance_dates = pd.date_range(start=returns.index[0], end=returns.index[-1], freq='MS')
    
    rebalance_dates = returns.index[returns.index.isin(rebalance_dates)]
    
    portfolio_returns = []
    current_selection = None
    
    for date in returns.index:
        # Vérifier si c'est une date de rebalancement
        if date in rebalance_dates:
            # Calculer le momentum
            start_idx = max(0, returns.index.get_loc(date) - lookback_days)
            hist_returns = returns.iloc[start_idx:returns.index.get_loc(date)]
            
            momentum = (1 + hist_returns).prod() - 1
            momentum = momentum.dropna().sort_values(ascending=False)
            
            # Sélectionner les top_n
            current_selection = momentum.head(top_n).index.tolist()
        
        # Calculer le rendement du jour
        if current_selection:
            day_return = returns.loc[date, current_selection].mean()
        else:
            day_return = 0
        
        portfolio_returns.append(day_return)
    
    portfolio_returns = pd.Series(portfolio_returns, index=returns.index)
    
    metrics = calculate_metrics(portfolio_returns)
    metrics['name'] = f"Momentum ({lookback_months}m, Top{top_n})"
    metrics['lookback'] = lookback_months
    metrics['top_n'] = top_n
    
    return metrics, portfolio_returns


def strategy_risk_parity(prices, vol_lookback_months=3, rebalance_freq='M'):
    """
    Stratégie Risk Parity - poids inverse de la volatilité
    """
    vol_lookback_days = vol_lookback_months * 21
    returns = prices.pct_change().dropna()
    
    if rebalance_freq == 'M':
        rebalance_dates = pd.date_range(start=returns.index[0], end=returns.index[-1], freq='MS')
    else:
        rebalance_dates = pd.date_range(start=returns.index[0], end=returns.index[-1], freq='QS')
    
    rebalance_dates = returns.index[returns.index.isin(rebalance_dates)]
    
    portfolio_returns = []
    current_weights = None
    
    for date in returns.index:
        if date in rebalance_dates:
            # Calculer la volatilité
            start_idx = max(0, returns.index.get_loc(date) - vol_lookback_days)
            hist_returns = returns.iloc[start_idx:returns.index.get_loc(date)]
            
            vol = hist_returns.std()
            vol = vol[vol > 0].dropna()
            
            # Poids = inverse de la volatilité
            inv_vol = 1 / vol
            current_weights = inv_vol / inv_vol.sum()
        
        # Rendement pondéré
        if current_weights is not None:
            available_tickers = [t for t in current_weights.index if t in returns.columns]
            weights = current_weights[available_tickers]
            weights = weights / weights.sum()  # Renormaliser
            day_return = (returns.loc[date, available_tickers] * weights).sum()
        else:
            day_return = 0
        
        portfolio_returns.append(day_return)
    
    portfolio_returns = pd.Series(portfolio_returns, index=returns.index)
    
    metrics = calculate_metrics(portfolio_returns)
    metrics['name'] = f"Risk Parity ({vol_lookback_months}m vol)"
    
    return metrics, portfolio_returns


def strategy_us_vs_world(prices, lookback_months=6):
    """
    Stratégie dynamique US vs Reste du monde
    Si momentum US > momentum World → 60% US, 40% Intl
    Sinon → 30% US, 70% Intl
    """
    lookback_days = lookback_months * 21
    returns = prices.pct_change().dropna()
    
    # Vérifier la disponibilité
    if 'SPY' not in returns.columns or 'ACWI' not in returns.columns:
        print("[!] Données SPY ou ACWI non disponibles pour cette stratégie")
        return None, None
    
    rebalance_dates = pd.date_range(start=returns.index[0], end=returns.index[-1], freq='MS')
    rebalance_dates = returns.index[returns.index.isin(rebalance_dates)]
    
    # ETF internationaux disponibles
    intl_etfs = [t for t in ['IEV', 'EWJ', 'EEM', 'VWO', 'EPP'] if t in returns.columns]
    
    portfolio_returns = []
    us_weight = 0.50  # Default
    intl_per_etf = 0.10 if intl_etfs else 0
    
    for date in returns.index:
        # Déterminer l'allocation
        if date in rebalance_dates:
            start_idx = max(0, returns.index.get_loc(date) - lookback_days)
            hist_returns = returns.iloc[start_idx:returns.index.get_loc(date)]
            
            momentum_spy = (1 + hist_returns['SPY']).prod() - 1
            momentum_acwi = (1 + hist_returns['ACWI']).prod() - 1
            
            if momentum_spy > momentum_acwi:
                us_weight = 0.60
            else:
                us_weight = 0.30
            
            intl_weight = 1 - us_weight
            intl_per_etf = intl_weight / len(intl_etfs) if intl_etfs else 0
        
        # Calculer le rendement
        day_return = returns.loc[date, 'SPY'] * us_weight
        for etf in intl_etfs:
            day_return += returns.loc[date, etf] * intl_per_etf
        
        portfolio_returns.append(day_return)
    
    portfolio_returns = pd.Series(portfolio_returns, index=returns.index)
    
    metrics = calculate_metrics(portfolio_returns)
    metrics['name'] = f"US vs World ({lookback_months}m)"
    
    return metrics, portfolio_returns


def analyze_correlations(prices):
    """Analyse des corrélations entre régions"""
    returns = prices.pct_change().dropna()
    corr = returns.corr()
    
    print("\n" + "="*70)
    print("MATRICE DE CORRÉLATION DES RENDEMENTS")
    print("="*70)
    print(corr.round(2).to_string())
    
    # Corrélation moyenne avec les US
    if 'SPY' in corr.columns:
        print("\nCorrélation avec S&P 500 (SPY):")
        for ticker in corr.columns:
            if ticker != 'SPY':
                print(f"  {ticker}: {corr.loc['SPY', ticker]:.2f}")
    
    return corr


def plot_cumulative_returns(all_returns, save_path='charts/geo_diversification_cumulative.png'):
    """Graphique des rendements cumulés"""
    os.makedirs('charts', exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(all_returns)))
    
    for i, (name, returns) in enumerate(all_returns.items()):
        cumulative = (1 + returns).cumprod()
        ax.plot(cumulative.index, cumulative, label=name, linewidth=2, color=colors[i])
    
    ax.set_title('Stratégies de Diversification Géographique - Performance Cumulée', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Valeur (base 1)')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"\n[OK] Graphique sauvegardé: {save_path}")
    plt.close()


def main():
    print("\n" + "="*70)
    print("TEST DE DIVERSIFICATION GÉOGRAPHIQUE")
    print("Réduction du risque US avec allocation multi-régions")
    print("="*70)
    
    # 1. Charger les données
    prices = load_geo_data(start_date='2007-01-01', end_date='2024-12-31')
    
    if prices.empty:
        print("[!] Erreur: pas de données disponibles")
        return
    
    # 2. Analyse des corrélations
    corr = analyze_correlations(prices)
    
    # 3. Tests des stratégies
    print("\n" + "="*70)
    print("TESTS DES STRATÉGIES")
    print("="*70)
    
    all_results = []
    all_returns = {}
    
    # 3.1 Benchmark: S&P 500
    if 'SPY' in prices.columns:
        spy_returns = prices['SPY'].pct_change().dropna()
        spy_metrics = calculate_metrics(spy_returns)
        spy_metrics['name'] = 'S&P 500 (Benchmark)'
        all_results.append(spy_metrics)
        all_returns['S&P 500'] = spy_returns
        print("\n[OK] S&P 500 charge comme benchmark")
    
    # 3.2 Benchmark: All Country World
    if 'ACWI' in prices.columns:
        acwi_returns = prices['ACWI'].pct_change().dropna()
        acwi_metrics = calculate_metrics(acwi_returns)
        acwi_metrics['name'] = 'MSCI All Country World'
        all_results.append(acwi_metrics)
        all_returns['ACWI World'] = acwi_returns
        print("[OK] MSCI ACWI charge")
    
    # 3.3 Buy & Hold Diversifié
    available_etfs = [t for t in ['SPY', 'IEV', 'EEM', 'EWJ'] if t in prices.columns]
    if len(available_etfs) >= 3:
        equal_weight = 1.0 / len(available_etfs)
        weights = {t: equal_weight for t in available_etfs}
        
        bh_metrics, bh_returns = strategy_buy_hold(prices, weights, "Equal Weight Global")
        all_results.append(bh_metrics)
        all_returns['Equal Weight'] = bh_returns
        print(f"[OK] Buy & Hold Equal Weight ({len(available_etfs)} regions)")
    
    # 3.4 Momentum Rotation
    if len(available_etfs) >= 3:
        mom_metrics, mom_returns = strategy_momentum_rotation(prices, lookback_months=12, top_n=2)
        all_results.append(mom_metrics)
        all_returns['Momentum (12m, Top2)'] = mom_returns
        print("[OK] Momentum Rotation (12 mois, Top 2)")
    
    # 3.5 Risk Parity
    if len(available_etfs) >= 3:
        rp_metrics, rp_returns = strategy_risk_parity(prices, vol_lookback_months=3)
        all_results.append(rp_metrics)
        all_returns['Risk Parity'] = rp_returns
        print("[OK] Risk Parity (3 mois vol)")
    
    # 3.6 US vs World Dynamique
    dyn_metrics, dyn_returns = strategy_us_vs_world(prices, lookback_months=6)
    if dyn_metrics:
        all_results.append(dyn_metrics)
        all_returns['US vs World Dynamic'] = dyn_returns
        print("[OK] US vs World Dynamique (6 mois)")
    
    # 4. Tableau comparatif
    print("\n" + "="*70)
    print("TABLEAU COMPARATIF DES STRATÉGIES")
    print("="*70)
    print(f"{'Stratégie':<30} {'Return':<10} {'Vol':<8} {'Sharpe':<8} {'Max DD':<10}")
    print("-"*70)
    
    for r in all_results:
        print(f"{r['name']:<30} {r['annualized_return']:>7.1f}%  "
              f"{r['volatility']:>6.1f}%  {r['sharpe_ratio']:>6.2f}  "
              f"{r['max_drawdown']:>7.1f}%")
    
    # 5. Graphique
    plot_cumulative_returns(all_returns)
    
    # 6. Analyse de la réduction du risque
    print("\n" + "="*70)
    print("ANALYSE DE LA RÉDUCTION DU RISQUE US")
    print("="*70)
    
    if 'S&P 500' in all_returns and len(all_results) > 1:
        spy_dd = all_results[0]['max_drawdown']
        print(f"\nDrawdown S&P 500: {spy_dd:.1f}%")
        print("\nStratégies avec drawdown réduit:")
        for r in all_results[1:]:
            dd_diff = r['max_drawdown'] - spy_dd  # Moins négatif = mieux
            if dd_diff > 0:  # Si drawdown moins sévère
                print(f"  [OK] {r['name']}: {r['max_drawdown']:.1f}% (amelioration de {dd_diff:.1f}pp)")
    
    # 7. Sauvegarder les résultats
    results_df = pd.DataFrame([{k: v for k, v in r.items() if k != 'weights'} for r in all_results])
    results_df.to_csv('data/geo_diversification_results.csv', index=False)
    print(f"\n[OK] Résultats sauvegardés: data/geo_diversification_results.csv")
    
    return all_results, all_returns


if __name__ == "__main__":
    results, returns = main()
