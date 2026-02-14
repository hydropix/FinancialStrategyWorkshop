#!/usr/bin/env python3
"""
Test de la strategie Momentum sur differents marches et periodes
US + Europe, periodes completes et crises
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from strategies.momentum import MomentumStrategy, MomentumConfig, run_monte_carlo_simulation


def load_us_data():
    """Charge les donnees US (S&P 500)"""
    print("\n[Chargement donnees US...]")
    from data.download_data import get_sp500_tickers, download_stock_data
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    return prices, "US S&P 500"


def load_eu_data():
    """Charge les donnees Europe (EURO STOXX)"""
    print("\n[Chargement donnees Europe...]")
    # Utiliser le fichier CSV existant
    eu_file = 'data/european_prices_clean.csv'
    if os.path.exists(eu_file):
        prices = pd.read_csv(eu_file, index_col=0, parse_dates=True)
        # Filtrer les colonnes avec suffisamment de donnees
        min_data = len(prices) * 0.8  # Au moins 80% de donnees
        valid_cols = prices.columns[prices.count() >= min_data]
        prices = prices[valid_cols].dropna(axis=0, how='all')
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        return prices, "Europe EURO STOXX"
    else:
        print(f"  Fichier non trouve: {eu_file}")
        return None, None


def load_eu_extended_data():
    """Charge les donnees Europe etendues (2007-2024)"""
    print("\n[Chargement donnees Europe etendues...]")
    eu_file = 'data/european_prices_2007_2024.csv'
    if os.path.exists(eu_file):
        prices = pd.read_csv(eu_file, index_col=0, parse_dates=True)
        valid_cols = prices.columns[prices.count() >= len(prices) * 0.7]
        prices = prices[valid_cols].dropna(axis=0, how='all')
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        return prices, "Europe 2007-2024"
    return None, None


def calculate_benchmark_metrics(prices):
    """Calcule les metriques du benchmark equipondere"""
    returns = prices.pct_change().mean(axis=1).dropna()
    cumulative = (1 + returns).cumprod()
    total_return = (cumulative.iloc[-1] - 1) * 100
    
    # Sharpe
    if returns.std() > 0:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    else:
        sharpe = 0
    
    # Max DD
    cummax = cumulative.cummax()
    drawdown = (cumulative - cummax) / cummax
    max_dd = drawdown.min() * 100
    
    # Volatilite
    vol = returns.std() * np.sqrt(252) * 100
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'volatility': vol
    }


def test_period(prices, period_name, start_date, end_date, config, n_sim=30):
    """Teste la strategie sur une periode specifique"""
    # S'assurer que l'index est un DatetimeIndex tz-naive
    prices = prices.copy()
    if not isinstance(prices.index, pd.DatetimeIndex):
        prices.index = pd.to_datetime(prices.index, utc=True).tz_localize(None)
    elif prices.index.tz is not None:
        prices.index = prices.index.tz_localize(None)
    
    # Convertir les dates en Timestamp
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    
    # Filtrer la periode
    period_prices = prices.loc[start_ts:end_ts]
    
    if len(period_prices) < 50:
        print(f"  [!] Periode {period_name} trop courte: {len(period_prices)} jours")
        return None
    
    # Benchmark
    bench = calculate_benchmark_metrics(period_prices)
    
    # Strategy - Monte Carlo
    mc_results = run_monte_carlo_simulation(
        prices=period_prices,
        n_simulations=n_sim,
        config=config
    )
    
    result = {
        'period': period_name,
        'market': '',
        'start': start_date,
        'end': end_date,
        'days': len(period_prices),
        'strat_return': mc_results['total_return'].mean(),
        'strat_sharpe': mc_results['sharpe_ratio'].mean(),
        'strat_dd': mc_results['max_drawdown'].mean(),
        'strat_vol': mc_results['volatility'].mean(),
        'bench_return': bench['total_return'],
        'bench_sharpe': bench['sharpe_ratio'],
        'bench_dd': bench['max_drawdown'],
        'outperformance': mc_results['total_return'].mean() - bench['total_return'],
        'sharpe_diff': mc_results['sharpe_ratio'].mean() - bench['sharpe_ratio'],
        'dd_diff': mc_results['max_drawdown'].mean() - bench['max_drawdown']
    }
    
    return result


def test_market(prices, market_name, config, periods_dict):
    """Teste un marche sur plusieurs periodes"""
    print(f"\n{'='*70}")
    print(f"TEST: {market_name}")
    print(f"{'='*70}")
    print(f"Periode totale: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Actions: {prices.shape[1]}")
    
    results = []
    for period_name, (start, end) in periods_dict.items():
        print(f"\n  >> Periode: {period_name} ({start} a {end})")
        result = test_period(prices, period_name, start, end, config)
        if result:
            result['market'] = market_name
            results.append(result)
            print(f"     Strategie: {result['strat_return']:.1f}% (Sharpe: {result['strat_sharpe']:.2f})")
            print(f"     Benchmark: {result['bench_return']:.1f}% (Sharpe: {result['bench_sharpe']:.2f})")
            print(f"     Surperf:   {result['outperformance']:+.1f}%")
    
    return pd.DataFrame(results)


def main():
    print("="*70)
    print("TEST MOMENTUM - MULTI-MARCHES & MULTI-PERIODES")
    print("="*70)
    
    # Configuration
    config = MomentumConfig(
        n_stocks=20,
        lookback_months=12,
        rebalancing_freq='M',
        init_cash=100_000,
        seed=42
    )
    
    print("\n[Configuration]")
    print(f"  Actions: {config.n_stocks}")
    print(f"  Lookback: {config.lookback_months} mois")
    print(f"  Rebalancement: Mensuel")
    
    all_results = []
    
    # ============================================================
    # 1. TEST US (2018-2024)
    # ============================================================
    us_prices, us_name = load_us_data()
    
    us_periods = {
        'Complete': ('2018-01-01', '2024-12-31'),
        'Pre-COVID': ('2018-01-01', '2020-02-01'),
        'COVID-Crise': ('2020-02-01', '2020-04-01'),
        'COVID-Recovery': ('2020-04-01', '2021-12-31'),
        'Bear Market 2022': ('2022-01-01', '2022-12-31'),
        'Bull 2023-2024': ('2023-01-01', '2024-12-31'),
    }
    
    us_results = test_market(us_prices, us_name, config, us_periods)
    if len(us_results) > 0:
        all_results.append(us_results)
    
    # ============================================================
    # 2. TEST EUROPE (2010-2024)
    # ============================================================
    eu_prices, eu_name = load_eu_data()
    
    if eu_prices is not None:
        eu_periods = {
            'Complete': (eu_prices.index[0].strftime('%Y-%m-%d'), eu_prices.index[-1].strftime('%Y-%m-%d')),
            '2010-2015': ('2010-01-01', '2015-12-31'),
            '2015-2020': ('2015-01-01', '2020-12-31'),
            '2020-2024': ('2020-01-01', '2024-12-31'),
        }
        
        eu_results = test_market(eu_prices, eu_name, config, eu_periods)
        if len(eu_results) > 0:
            all_results.append(eu_results)
    
    # ============================================================
    # 3. TEST EUROPE ETENDU (2007-2024) - Crise 2008
    # ============================================================
    eu_ext_prices, eu_ext_name = load_eu_extended_data()
    
    if eu_ext_prices is not None and len(eu_ext_prices) > 0:
        start_str = eu_ext_prices.index[0].strftime('%Y-%m-%d') if hasattr(eu_ext_prices.index[0], 'strftime') else str(eu_ext_prices.index[0])[:10]
        end_str = eu_ext_prices.index[-1].strftime('%Y-%m-%d') if hasattr(eu_ext_prices.index[-1], 'strftime') else str(eu_ext_prices.index[-1])[:10]
        eu_ext_periods = {
            'Complete': (start_str, end_str),
            'Financial Crisis': ('2007-01-01', '2009-12-31'),
            'Post-Crisis': ('2010-01-01', '2014-12-31'),
            'Recent': ('2015-01-01', '2024-12-31'),
        }
        
        eu_ext_results = test_market(eu_ext_prices, eu_ext_name, config, eu_ext_periods)
        if len(eu_ext_results) > 0:
            all_results.append(eu_ext_results)
    
    # ============================================================
    # RESUME GLOBAL
    # ============================================================
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        
        print("\n" + "="*70)
        print("TABLEAU RECAPITULATIF COMPLET")
        print("="*70)
        
        # Afficher le tableau
        display_cols = ['market', 'period', 'strat_return', 'bench_return', 'outperformance', 
                       'strat_sharpe', 'bench_sharpe', 'strat_dd', 'bench_dd']
        
        for _, row in combined.iterrows():
            print(f"\n{row['market']} - {row['period']}")
            print(f"  Strategie:  Return={row['strat_return']:6.1f}%  Sharpe={row['strat_sharpe']:.2f}  DD={row['strat_dd']:6.1f}%")
            print(f"  Benchmark:  Return={row['bench_return']:6.1f}%  Sharpe={row['bench_sharpe']:.2f}  DD={row['bench_dd']:6.1f}%")
            perf = row['outperformance']
            symbol = "+" if perf > 0 else ""
            print(f"  Surperf:    {symbol}{perf:5.1f}%")
        
        # Sauvegarder
        output_file = 'data/momentum_multimarket_results.csv'
        combined.to_csv(output_file, index=False)
        print(f"\n[OK] Resultats sauvegardes dans: {output_file}")
        
        # Statistiques globales
        print("\n" + "="*70)
        print("STATISTIQUES GLOBALES")
        print("="*70)
        
        wins = (combined['outperformance'] > 0).sum()
        total = len(combined)
        print(f"Surperformance positive: {wins}/{total} periodes ({wins/total*100:.0f}%)")
        print(f"Surperformance moyenne: {combined['outperformance'].mean():.1f}%")
        print(f"Meilleure surperf: {combined['outperformance'].max():.1f}%")
        print(f"Pire surperf: {combined['outperformance'].min():.1f}%")
        
        # Par marche
        print("\n[Par marche]")
        for market in combined['market'].unique():
            market_data = combined[combined['market'] == market]
            print(f"  {market}: {market_data['outperformance'].mean():+.1f}% en moyenne")
        
        # Par periode de crise vs expansion
        crisis_periods = ['COVID-Crise', 'Financial Crisis', 'Bear Market 2022']
        expansion_periods = ['COVID-Recovery', 'Bull 2023-2024', 'Post-Crisis']
        
        crisis_data = combined[combined['period'].isin(crisis_periods)]
        expansion_data = combined[combined['period'].isin(expansion_periods)]
        
        if len(crisis_data) > 0:
            print(f"\n  Periodes de crise: {crisis_data['outperformance'].mean():+.1f}% en moyenne")
        if len(expansion_data) > 0:
            print(f"  Periodes d'expansion: {expansion_data['outperformance'].mean():+.1f}% en moyenne")
        
        return combined
    
    return None


if __name__ == "__main__":
    results = main()
