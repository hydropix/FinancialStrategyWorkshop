#!/usr/bin/env python3
"""
Test de la configuration Momentum OPTIMALE sur le marché Europe
Config: 10 actions, 3 mois lookback, rebalancement trimestriel
Periodes: 2010-2024 avec sous-periodes historiques
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from strategies.momentum import MomentumStrategy, MomentumConfig


def load_europe_data():
    """Charge les donnees Europe"""
    print("\n[Chargement donnees Europe EURO STOXX...]")
    
    # Fichier principal
    eu_file = 'data/european_prices_clean.csv'
    if os.path.exists(eu_file):
        prices = pd.read_csv(eu_file, index_col=0, parse_dates=True)
        
        # Nettoyage
        min_data = len(prices) * 0.7
        valid_cols = prices.columns[prices.count() >= min_data]
        prices = prices[valid_cols].dropna(axis=0, how='all')
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        
        # Tz-naive
        if prices.index.tz is not None:
            prices.index = prices.index.tz_localize(None)
        
        print(f"  Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
        print(f"  Actions: {prices.shape[1]}")
        return prices
    return None


def load_europe_extended():
    """Charge les donnees Europe etendues (2007-2024)"""
    print("\n[Chargement donnees Europe etendues (2007-2024)...]")
    
    eu_file = 'data/european_prices_2007_2024.csv'
    if os.path.exists(eu_file):
        prices = pd.read_csv(eu_file, index_col=0, parse_dates=True)
        
        min_data = len(prices) * 0.5
        valid_cols = prices.columns[prices.count() >= min_data]
        prices = prices[valid_cols]
        
        if len(prices.columns) == 0 or len(prices) == 0:
            print("  [!] Donnees insuffisantes apres filtrage")
            return None
        
        prices = prices.dropna(axis=0, how='all')
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        
        if prices.index.tz is not None:
            prices.index = prices.index.tz_localize(None)
        
        if len(prices.index) > 0:
            print(f"  Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
            print(f"  Actions: {prices.shape[1]}")
            return prices
    return None


def calculate_benchmark_metrics(prices):
    """Calcule les metriques du benchmark equipondere"""
    returns = prices.pct_change().mean(axis=1).dropna()
    cumulative = (1 + returns).cumprod()
    
    total_return = (cumulative.iloc[-1] - 1) * 100
    
    if returns.std() > 0:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    else:
        sharpe = 0
    
    cummax = cumulative.cummax()
    drawdown = (cumulative - cummax) / cummax
    max_dd = drawdown.min() * 100
    
    vol = returns.std() * np.sqrt(252) * 100
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'volatility': vol
    }


def test_period(prices, period_name, start_date, end_date, config, n_sim=30):
    """Teste une periode specifique"""
    # Convertir dates
    if isinstance(prices.index, pd.DatetimeIndex) and prices.index.tz is not None:
        prices = prices.copy()
        prices.index = prices.index.tz_localize(None)
    
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    
    # Filtrer
    period_prices = prices.loc[start_ts:end_ts]
    
    if len(period_prices) < 100:
        print(f"  [!] Periode {period_name} trop courte: {len(period_prices)} jours")
        return None
    
    # Benchmark
    bench = calculate_benchmark_metrics(period_prices)
    
    # Strategy
    results = []
    for i in range(n_sim):
        sim_config = MomentumConfig(
            n_stocks=config.n_stocks,
            lookback_months=config.lookback_months,
            rebalancing_freq=config.rebalancing_freq,
            init_cash=100_000,
            seed=i
        )
        
        strategy = MomentumStrategy(sim_config)
        result = strategy.run_backtest_simple(period_prices, verbose=False)
        
        if result:
            results.append({
                'total_return': result['total_return'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'n_transactions': result['n_transactions']
            })
    
    if len(results) == 0:
        return None
    
    df = pd.DataFrame(results)
    
    return {
        'period': period_name,
        'start': start_date,
        'end': end_date,
        'days': len(period_prices),
        'strat_return': df['total_return'].mean(),
        'strat_sharpe': df['sharpe_ratio'].mean(),
        'strat_dd': df['max_drawdown'].mean(),
        'strat_txn': df['n_transactions'].mean(),
        'bench_return': bench['total_return'],
        'bench_sharpe': bench['sharpe_ratio'],
        'bench_dd': bench['max_drawdown'],
        'outperformance': df['total_return'].mean() - bench['total_return']
    }


def main():
    print("="*70)
    print("TEST MOMENTUM OPTIMAL (10, 3M, Q) SUR MARCHE EUROPE")
    print("="*70)
    print("\nConfiguration optimale:")
    print("  - N actions: 10")
    print("  - Lookback: 3 mois")
    print("  - Rebalancement: Trimestriel")
    
    config = MomentumConfig(
        n_stocks=10,
        lookback_months=3,
        rebalancing_freq='Q',
        init_cash=100_000
    )
    
    all_results = []
    
    # ============================================================
    # 1. TEST EUROPE 2010-2024
    # ============================================================
    eu_prices = load_europe_data()
    
    if eu_prices is not None:
        print("\n" + "="*70)
        print("TEST EUROPE 2010-2024")
        print("="*70)
        
        periods = {
            'Complete 2010-2024': ('2010-06-01', '2024-12-31'),
            'Crise Euro 2010-2012': ('2010-01-01', '2012-12-31'),
            'Recovery 2012-2015': ('2012-01-01', '2015-12-31'),
            'Brexit 2015-2017': ('2015-01-01', '2017-12-31'),
            'Bull 2017-2020': ('2017-01-01', '2020-02-01'),
            'COVID Crise': ('2020-02-01', '2020-04-01'),
            'COVID Recovery': ('2020-04-01', '2021-12-31'),
            'Inflation/Guerre 2022-2024': ('2022-01-01', '2024-12-31'),
        }
        
        for name, (start, end) in periods.items():
            print(f"\n  >> {name}")
            result = test_period(eu_prices, name, start, end, config)
            if result:
                result['market'] = 'Europe 2010-2024'
                all_results.append(result)
                print(f"     Strategie: {result['strat_return']:6.1f}% (Sharpe: {result['strat_sharpe']:.2f})")
                print(f"     Benchmark: {result['bench_return']:6.1f}% (Sharpe: {result['bench_sharpe']:.2f})")
                print(f"     Surperf:   {result['outperformance']:+6.1f}%")
    
    # ============================================================
    # 2. TEST EUROPE ETENDU 2007-2024 (avec crise financiere)
    # ============================================================
    eu_ext_prices = load_europe_extended()
    
    if eu_ext_prices is not None and len(eu_ext_prices) > 0 and len(eu_ext_prices.columns) > 0:
        print("\n" + "="*70)
        print("TEST EUROPE ETENDU 2007-2024 (Crise Financiere)")
        print("="*70)
        
        start_str = eu_ext_prices.index[0].strftime('%Y-%m-%d') if len(eu_ext_prices.index) > 0 else 'N/A'
        end_str = eu_ext_prices.index[-1].strftime('%Y-%m-%d') if len(eu_ext_prices.index) > 0 else 'N/A'
        
        periods_ext = {
            'Complete 2007-2024': (start_str, end_str),
            'Financial Crisis': ('2007-01-01', '2009-12-31'),
            'Post-Crisis Recovery': ('2009-01-01', '2013-12-31'),
            'Recent 2015-2024': ('2015-01-01', '2024-12-31'),
        }
        
        for name, (start, end) in periods_ext.items():
            print(f"\n  >> {name}")
            result = test_period(eu_ext_prices, name, start, end, config)
            if result:
                result['market'] = 'Europe 2007-2024'
                all_results.append(result)
                print(f"     Strategie: {result['strat_return']:6.1f}% (Sharpe: {result['strat_sharpe']:.2f})")
                print(f"     Benchmark: {result['bench_return']:6.1f}% (Sharpe: {result['bench_sharpe']:.2f})")
                print(f"     Surperf:   {result['outperformance']:+6.1f}%")
    
    # ============================================================
    # TABLEAU RECAPITULATIF
    # ============================================================
    if all_results:
        df = pd.DataFrame(all_results)
        
        print("\n" + "="*70)
        print("TABLEAU RECAPITULATIF COMPLET - EUROPE")
        print("="*70)
        print(f"\n{'Periode':<25} {'Strategie':<10} {'Benchmark':<10} {'Surperf':<10} {'Sharpe':<8}")
        print("-"*70)
        
        for _, row in df.iterrows():
            print(f"{row['period']:<25} {row['strat_return']:>8.1f}% {row['bench_return']:>8.1f}% "
                  f"{row['outperformance']:>+8.1f}% {row['strat_sharpe']:>7.2f}")
        
        # Sauvegarde
        df.to_csv('data/momentum_europe_optimal_results.csv', index=False)
        print("\n[OK] Resultats sauvegardes: data/momentum_europe_optimal_results.csv")
        
        # Statistiques
        print("\n" + "="*70)
        print("STATISTIQUES GLOBALES - EUROPE")
        print("="*70)
        
        wins = (df['outperformance'] > 0).sum()
        total = len(df)
        print(f"\nSurperformance positive: {wins}/{total} periodes ({wins/total*100:.0f}%)")
        print(f"Surperformance moyenne: {df['outperformance'].mean():+.1f}%")
        print(f"Meilleure surperf: {df['outperformance'].max():+.1f}%")
        print(f"Pire surperf: {df['outperformance'].min():+.1f}%")
        
        # Par type de periode
        crisis_periods = ['Financial Crisis', 'COVID Crise', 'Crise Euro 2010-2012']
        expansion_periods = ['Bull 2017-2020', 'COVID Recovery', 'Recovery 2012-2015']
        
        crisis_data = df[df['period'].isin(crisis_periods)]
        expansion_data = df[df['period'].isin(expansion_periods)]
        
        if len(crisis_data) > 0:
            print(f"\n  Periodes de crise: {crisis_data['outperformance'].mean():+.1f}% en moyenne")
        if len(expansion_data) > 0:
            print(f"  Periodes d'expansion: {expansion_data['outperformance'].mean():+.1f}% en moyenne")
        
        return df
    
    return None


if __name__ == "__main__":
    results = main()
