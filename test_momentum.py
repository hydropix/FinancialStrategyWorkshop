#!/usr/bin/env python3
"""
Script de test complet pour la strategie Momentum
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from strategies.momentum import MomentumStrategy, MomentumConfig, run_monte_carlo_simulation


def calculate_benchmark(prices: pd.DataFrame) -> dict:
    """Calcule les metriques du benchmark (Buy & Hold equi-poids)"""
    # Rendement moyen de toutes les actions (equi-poids)
    returns = prices.pct_change().mean(axis=1)
    cumulative = (1 + returns).cumprod()
    total_return = (cumulative.iloc[-1] - 1) * 100
    
    # Sharpe ratio
    if returns.std() > 0:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    else:
        sharpe = 0
    
    # Max drawdown
    cummax = cumulative.cummax()
    drawdown = (cumulative - cummax) / cummax
    max_dd = drawdown.min() * 100
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd
    }


def main():
    print("="*70)
    print("TEST STRATEGIE MOMENTUM")
    print("="*70)
    print("\nConcept: Selectionner les actions avec les meilleures performances")
    print("sur les 12 derniers mois, rebalancement mensuel")
    
    # 1. Chargement des donnees
    print("\n" + "-"*70)
    print("[1/5] Chargement des donnees S&P 500...")
    print("-"*70)
    
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    
    print(f"  Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"  Nombre d'actions: {len(prices.columns)}")
    print(f"  Nombre de jours: {len(prices)}")
    
    # 2. Configuration
    print("\n" + "-"*70)
    print("[2/5] Configuration de la strategie...")
    print("-"*70)
    
    config = MomentumConfig(
        n_stocks=20,              # Top 20 actions
        lookback_months=12,       # Performance sur 12 mois
        rebalancing_freq='M',     # Rebalancement mensuel
        init_cash=100_000,
        seed=42
    )
    
    print(f"  Nombre d'actions: {config.n_stocks}")
    print(f"  Lookback: {config.lookback_months} mois")
    print(f"  Rebalancement: {config.rebalancing_freq} (Mensuel)")
    print(f"  Capital initial: ${config.init_cash:,.2f}")
    
    # 3. Test individuel
    print("\n" + "-"*70)
    print("[3/5] Test individuel (1 simulation)...")
    print("-"*70)
    
    strategy = MomentumStrategy(config)
    result = strategy.run_backtest_simple(prices, verbose=True)
    
    # 4. Monte Carlo
    print("\n" + "-"*70)
    print("[4/5] Monte Carlo (50 simulations)...")
    print("-"*70)
    
    mc_results = run_monte_carlo_simulation(
        prices=prices,
        n_simulations=50,
        config=config
    )
    
    # 5. Analyse statistique
    print("\n" + "-"*70)
    print("[5/5] Analyse statistique et comparaison avec benchmark...")
    print("-"*70)
    
    # Benchmark
    benchmark = calculate_benchmark(prices)
    
    print("\n[RESULTATS MOMENTUM (Moyenne Monte Carlo)]")
    print(f"  Rendement moyen:  {mc_results['total_return'].mean():.2f}%")
    print(f"  Sharpe moyen:     {mc_results['sharpe_ratio'].mean():.2f}")
    print(f"  Max drawdown:     {mc_results['max_drawdown'].mean():.2f}%")
    print(f"  Volatilite:       {mc_results['volatility'].mean():.2f}%")
    print(f"  Transactions:     {mc_results['n_transactions'].mean():.0f}")
    
    print("\n[BENCHMARK (Buy & Hold Equi-poids)]")
    print(f"  Rendement:        {benchmark['total_return']:.2f}%")
    print(f"  Sharpe:           {benchmark['sharpe_ratio']:.2f}")
    print(f"  Max drawdown:     {benchmark['max_drawdown']:.2f}%")
    
    # Comparaison
    alpha = mc_results['total_return'].mean() - benchmark['total_return']
    print("\n[COMPARAISON]")
    print(f"  Surperformance:   {alpha:+.2f}% ({'+' if alpha > 0 else ''}{alpha/benchmark['total_return']*100:.1f}% relatif)")
    print(f"  Sharpe vs Bench:  {mc_results['sharpe_ratio'].mean() - benchmark['sharpe_ratio']:+.2f}")
    print(f"  Protection DD:    {mc_results['max_drawdown'].mean() - benchmark['max_drawdown']:+.2f}%")
    
    # Variabilite
    print("\n[ROBUSTESSE - ecart-type des simulations]")
    print(f"  Std rendement:    {mc_results['total_return'].std():.2f}%")
    print(f"  Min rendement:    {mc_results['total_return'].min():.2f}%")
    print(f"  Max rendement:    {mc_results['total_return'].max():.2f}%")
    
    # Sauvegarder les resultats
    output_file = 'data/momentum_results.csv'
    mc_results.to_csv(output_file, index=False)
    print(f"\n[OK] Resultats sauvegardes dans: {output_file}")
    
    # Resume final
    print("\n" + "="*70)
    print("RESUME FINAL")
    print("="*70)
    
    if alpha > 0:
        print("[OK] La strategie MOMENTUM SURPERFORME le benchmark!")
    else:
        print("[NO] La strategie MOMENTUM ne surperforme pas le benchmark")
    
    if mc_results['sharpe_ratio'].mean() > benchmark['sharpe_ratio']:
        print("[OK] Meilleur ratio de Sharpe (meilleur rendement ajuste au risque)")
    else:
        print("[!] Ratio de Sharpe inferieur au benchmark")
    
    if mc_results['max_drawdown'].mean() > benchmark['max_drawdown']:
        print("[OK] Drawdown mieux controle que le benchmark")
    else:
        print("[!] Drawdown plus severe que le benchmark")
    
    return mc_results, benchmark


if __name__ == "__main__":
    results, benchmark = main()
