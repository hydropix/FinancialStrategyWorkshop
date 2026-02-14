#!/usr/bin/env python3
"""
Optimisation des hyperparametres de la strategie Momentum
Grid Search complet sur:
- Nombre d'actions (n_stocks)
- Periode de lookback (lookback_months)
- Frequence de rebalancement (rebalancing_freq)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import itertools
import time
import warnings
warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from strategies.momentum import MomentumStrategy, MomentumConfig


def calculate_benchmark(prices):
    """Calcule le rendement du benchmark equipondere"""
    returns = prices.pct_change().mean(axis=1).dropna()
    cumulative = (1 + returns).cumprod()
    return (cumulative.iloc[-1] - 1) * 100


def test_configuration(prices, config, n_simulations=30):
    """Teste une configuration specifique"""
    results = []
    
    for i in range(n_simulations):
        sim_config = MomentumConfig(
            n_stocks=config.n_stocks,
            lookback_months=config.lookback_months,
            rebalancing_freq=config.rebalancing_freq,
            init_cash=config.init_cash,
            seed=i
        )
        
        strategy = MomentumStrategy(sim_config)
        result = strategy.run_backtest_simple(prices, verbose=False)
        
        if result:
            results.append({
                'total_return': result['total_return'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'volatility': result['volatility'],
                'n_transactions': result['n_transactions']
            })
    
    if len(results) == 0:
        return None
    
    df = pd.DataFrame(results)
    return {
        'total_return_mean': df['total_return'].mean(),
        'total_return_std': df['total_return'].std(),
        'sharpe_ratio_mean': df['sharpe_ratio'].mean(),
        'max_drawdown_mean': df['max_drawdown'].mean(),
        'volatility_mean': df['volatility'].mean(),
        'n_transactions_mean': df['n_transactions'].mean()
    }


def main():
    print("="*70)
    print("OPTIMISATION GRID SEARCH - STRATEGIE MOMENTUM")
    print("="*70)
    
    # Chargement des donnees
    print("\n[1] Chargement des donnees S&P 500...")
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2010-01-01', end_date='2024-12-31')
    
    print(f"  Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"  Actions: {prices.shape[1]}")
    
    # Benchmark
    benchmark_return = calculate_benchmark(prices)
    print(f"  Benchmark (Buy & Hold): {benchmark_return:.1f}%")
    
    # ============================================================
    # GRID SEARCH PARAMETRES
    # ============================================================
    print("\n[2] Configuration du Grid Search...")
    
    # Parametres a tester
    param_grid = {
        'n_stocks': [10, 20, 30],           # Nombre d'actions
        'lookback_months': [3, 6, 9, 12],   # Periode de lookback
        'rebalancing_freq': ['M', 'Q']      # Mensuel, Trimestriel
    }
    
    # Generer toutes les combinaisons
    combinations = list(itertools.product(
        param_grid['n_stocks'],
        param_grid['lookback_months'],
        param_grid['rebalancing_freq']
    ))
    
    print(f"  Nombre de configurations a tester: {len(combinations)}")
    print(f"  Simulations par config: 30")
    print(f"  Total simulations: {len(combinations) * 30}")
    
    print("\n  Parametres:")
    print(f"    - N actions: {param_grid['n_stocks']}")
    print(f"    - Lookback (mois): {param_grid['lookback_months']}")
    print(f"    - Rebalancement: {param_grid['rebalancing_freq']}")
    
    # ============================================================
    # EXECUTION
    # ============================================================
    print("\n[3] Execution du Grid Search...")
    print("="*70)
    
    results = []
    start_time = time.time()
    
    for idx, (n_stocks, lookback, freq) in enumerate(combinations):
        print(f"\n[{idx+1}/{len(combinations)}] Testing: N={n_stocks}, Lookback={lookback}mo, Freq={freq}")
        
        config = MomentumConfig(
            n_stocks=n_stocks,
            lookback_months=lookback,
            rebalancing_freq=freq,
            init_cash=100_000
        )
        
        result = test_configuration(prices, config, n_simulations=30)
        
        if result:
            result['n_stocks'] = n_stocks
            result['lookback_months'] = lookback
            result['rebalancing_freq'] = freq
            result['outperformance'] = result['total_return_mean'] - benchmark_return
            results.append(result)
            
            print(f"  -> Return: {result['total_return_mean']:.1f}% | "
                  f"Sharpe: {result['sharpe_ratio_mean']:.2f} | "
                  f"DD: {result['max_drawdown_mean']:.1f}% | "
                  f"Surperf: {result['outperformance']:+.1f}%")
    
    elapsed = time.time() - start_time
    print(f"\n[OK] Grid Search termine en {elapsed/60:.1f} minutes")
    
    # ============================================================
    # ANALYSE DES RESULTATS
    # ============================================================
    print("\n[4] Analyse des resultats...")
    print("="*70)
    
    df_results = pd.DataFrame(results)
    
    # Sauvegarder tous les resultats
    output_file = 'data/momentum_grid_search.csv'
    df_results.to_csv(output_file, index=False)
    print(f"[OK] Resultats sauvegardes dans: {output_file}")
    
    # TOP 10 par rendement
    print("\n--- TOP 10 PAR RENDEMENT ---")
    top_return = df_results.nlargest(10, 'total_return_mean')[
        ['n_stocks', 'lookback_months', 'rebalancing_freq', 
         'total_return_mean', 'sharpe_ratio_mean', 'outperformance']
    ]
    for i, row in top_return.iterrows():
        print(f"  N={row['n_stocks']:2d}, LB={row['lookback_months']:2d}mo, F={row['rebalancing_freq']} | "
              f"Return={row['total_return_mean']:6.1f}% | Sharpe={row['sharpe_ratio_mean']:.2f} | "
              f"Surperf={row['outperformance']:+6.1f}%")
    
    # TOP 10 par Sharpe ratio
    print("\n--- TOP 10 PAR SHARPE RATIO ---")
    top_sharpe = df_results.nlargest(10, 'sharpe_ratio_mean')[
        ['n_stocks', 'lookback_months', 'rebalancing_freq', 
         'total_return_mean', 'sharpe_ratio_mean', 'outperformance']
    ]
    for i, row in top_sharpe.iterrows():
        print(f"  N={row['n_stocks']:2d}, LB={row['lookback_months']:2d}mo, F={row['rebalancing_freq']} | "
              f"Sharpe={row['sharpe_ratio_mean']:5.2f} | Return={row['total_return_mean']:6.1f}% | "
              f"Surperf={row['outperformance']:+6.1f}%")
    
    # TOP 10 par surperformance
    print("\n--- TOP 10 PAR SURPERFORMANCE ---")
    top_outperf = df_results.nlargest(10, 'outperformance')[
        ['n_stocks', 'lookback_months', 'rebalancing_freq', 
         'total_return_mean', 'sharpe_ratio_mean', 'outperformance']
    ]
    for i, row in top_outperf.iterrows():
        print(f"  N={row['n_stocks']:2d}, LB={row['lookback_months']:2d}mo, F={row['rebalancing_freq']} | "
              f"Surperf={row['outperformance']:+6.1f}% | Return={row['total_return_mean']:6.1f}% | "
              f"Sharpe={row['sharpe_ratio_mean']:.2f}")
    
    # CONFIGURATION OPTIMALE
    print("\n" + "="*70)
    print("CONFIGURATION OPTIMALE IDENTIFIEE")
    print("="*70)
    
    # Meilleure surperformance
    best_outperf = df_results.loc[df_results['outperformance'].idxmax()]
    print("\n[Par Surperformance vs Benchmark]:")
    print(f"  N actions:         {best_outperf['n_stocks']}")
    print(f"  Lookback:          {best_outperf['lookback_months']} mois")
    print(f"  Rebalancement:     {best_outperf['rebalancing_freq']} ({'Mensuel' if best_outperf['rebalancing_freq']=='M' else 'Trimestriel'})")
    print(f"  Rendement:         {best_outperf['total_return_mean']:.1f}%")
    print(f"  Sharpe Ratio:      {best_outperf['sharpe_ratio_mean']:.2f}")
    print(f"  Max Drawdown:      {best_outperf['max_drawdown_mean']:.1f}%")
    print(f"  Transactions:      {best_outperf['n_transactions_mean']:.0f}")
    print(f"  Surperformance:    {best_outperf['outperformance']:+.1f}%")
    
    # Meilleur Sharpe
    best_sharpe = df_results.loc[df_results['sharpe_ratio_mean'].idxmax()]
    print("\n[Par Sharpe Ratio]:")
    print(f"  N actions:         {best_sharpe['n_stocks']}")
    print(f"  Lookback:          {best_sharpe['lookback_months']} mois")
    print(f"  Rebalancement:     {best_sharpe['rebalancing_freq']}")
    print(f"  Rendement:         {best_sharpe['total_return_mean']:.1f}%")
    print(f"  Sharpe Ratio:      {best_sharpe['sharpe_ratio_mean']:.2f}")
    print(f"  Surperformance:    {best_sharpe['outperformance']:+.1f}%")
    
    # Analyse par parametre
    print("\n" + "="*70)
    print("ANALYSE PAR PARAMETRE")
    print("="*70)
    
    print("\n[Impact du nombre d'actions]:")
    for n in param_grid['n_stocks']:
        subset = df_results[df_results['n_stocks'] == n]
        print(f"  N={n:2d}: Return={subset['total_return_mean'].mean():6.1f}% | "
              f"Sharpe={subset['sharpe_ratio_mean'].mean():.2f} | "
              f"Surperf={subset['outperformance'].mean():+6.1f}%")
    
    print("\n[Impact du lookback]:")
    for lb in param_grid['lookback_months']:
        subset = df_results[df_results['lookback_months'] == lb]
        print(f"  LB={lb:2d}mo: Return={subset['total_return_mean'].mean():6.1f}% | "
              f"Sharpe={subset['sharpe_ratio_mean'].mean():.2f} | "
              f"Surperf={subset['outperformance'].mean():+6.1f}%")
    
    print("\n[Impact de la frequence]:")
    for freq in param_grid['rebalancing_freq']:
        subset = df_results[df_results['rebalancing_freq'] == freq]
        label = 'Mensuel' if freq == 'M' else 'Trimestriel'
        print(f"  {label}: Return={subset['total_return_mean'].mean():6.1f}% | "
              f"Sharpe={subset['sharpe_ratio_mean'].mean():.2f} | "
              f"Surperf={subset['outperformance'].mean():+6.1f}%")
    
    return df_results


if __name__ == "__main__":
    results = main()
