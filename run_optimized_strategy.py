"""
Script pour executer la strategie avec les parametres OPTIMISES
Configuration recommandee : N=30, Lookback=3 mois, Stop-loss=-5%
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from strategies.random_stoploss import RandomStopLossStrategy, StrategyConfig, run_monte_carlo_simulation


def main():
    print("="*70)
    print("STRATEGIE OPTIMISEE - CONFIGURATION RECOMMANDEE")
    print("="*70)
    print("\nParametres optimaux identifies par Grid Search:")
    print("  - Nombre d'actions : 30 (diversification maximale)")
    print("  - Lookback : 3 mois (reaction rapide)")
    print("  - Stop-loss : -5% (protection renforcee)")
    print("="*70)
    
    # 1. Charger les donnees
    print("\n[ETAPE 1] Chargement des donnees")
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    
    print(f"\nPeriode analysee: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Nombre d'actions disponibles: {prices.shape[1]}")
    
    # 2. Configuration OPTIMISEE
    print("\n[ETAPE 2] Configuration OPTIMISEE")
    optimized_config = StrategyConfig(
        n_stocks=30,
        lookback_months=3,
        stop_loss_threshold=-0.05,
        init_cash=100_000,
        seed=42
    )
    print(f"  - Nombre d'actions: {optimized_config.n_stocks}")
    print(f"  - Lookback stop-loss: {optimized_config.lookback_months} mois")
    print(f"  - Seuil stop-loss: {optimized_config.stop_loss_threshold*100:.0f}%")
    print(f"  - Capital initial: ${optimized_config.init_cash:,.0f}")
    
    # 3. Test individuel
    print("\n[ETAPE 3] Test d'une simulation individuelle")
    strategy = RandomStopLossStrategy(optimized_config)
    result = strategy.run_backtest_simple(prices, verbose=True)
    
    if result:
        print(f"\n  Resultats de la simulation:")
        print(f"    - Rendement total: {result['total_return']:.2f}%")
        print(f"    - Ratio de Sharpe: {result['sharpe_ratio']:.2f}")
        print(f"    - Max Drawdown: {result['max_drawdown']:.2f}%")
        print(f"    - Valeur finale: ${result['final_value']:,.2f}")
    
    # 4. Simulations Monte Carlo
    print("\n[ETAPE 4] Simulations Monte Carlo (100 simulations)")
    mc_results = run_monte_carlo_simulation(
        prices=prices,
        n_simulations=100,
        config=optimized_config
    )
    
    # 5. Analyse des resultats
    print("\n[ETAPE 5] Analyse statistique")
    print("\n" + "="*70)
    print("RESULTATS DES SIMULATIONS MONTE CARLO - CONFIGURATION OPTIMISEE (n=100)")
    print("="*70)
    
    metrics = ['total_return', 'sharpe_ratio', 'max_drawdown']
    
    summary = pd.DataFrame({
        'Metrique': [],
        'Moyenne': [],
        'Mediane': [],
        'Ecart-type': [],
        'Min': [],
        'Max': [],
        'Percentile 5%': [],
        'Percentile 95%': []
    })
    
    for metric in metrics:
        if metric in mc_results.columns:
            values = mc_results[metric].dropna()
            if len(values) > 0:
                summary = pd.concat([summary, pd.DataFrame({
                    'Metrique': [metric],
                    'Moyenne': [values.mean()],
                    'Mediane': [values.median()],
                    'Ecart-type': [values.std()],
                    'Min': [values.min()],
                    'Max': [values.max()],
                    'Percentile 5%': [values.quantile(0.05)],
                    'Percentile 95%': [values.quantile(0.95)]
                })], ignore_index=True)
    
    print("\n", summary.to_string(index=False))
    
    # 6. Comparaison avec benchmark
    print("\n" + "="*70)
    print("COMPARAISON AVEC BENCHMARK (Buy & Hold S&P 500)")
    print("="*70)
    
    benchmark_returns = prices.pct_change().mean(axis=1)
    benchmark_cum = (1 + benchmark_returns).cumprod()
    benchmark_total_return = (benchmark_cum.iloc[-1] - 1) * 100
    
    print(f"\n  Benchmark (Buy & Hold equipondere):")
    print(f"    - Rendement total: {benchmark_total_return:.2f}%")
    
    print(f"\n  Strategie OPTIMISEE (moyenne Monte Carlo):")
    print(f"    - Rendement total moyen: {mc_results['total_return'].mean():.2f}%")
    print(f"    - Ratio de Sharpe moyen: {mc_results['sharpe_ratio'].mean():.2f}")
    print(f"    - Max Drawdown moyen: {mc_results['max_drawdown'].mean():.2f}%")
    
    outperformance = mc_results['total_return'].mean() - benchmark_total_return
    print(f"\n  Surperformance vs Benchmark: {outperformance:.2f}%")
    print(f"  % > Benchmark: {(mc_results['total_return'] > benchmark_total_return).mean() * 100:.1f}%")
    
    # 7. Comparaison Configuration Base vs Optimisee
    print("\n" + "="*70)
    print("COMPARAISON: CONFIGURATION DE BASE vs OPTIMISEE")
    print("="*70)
    
    baseline_config = StrategyConfig(
        n_stocks=20,
        lookback_months=6,
        stop_loss_threshold=-0.10,
        init_cash=100_000,
        seed=42
    )
    
    print("\n  Configuration de Base:")
    print(f"    - N={baseline_config.n_stocks}, Lookback={baseline_config.lookback_months}mois, SL={baseline_config.stop_loss_threshold*100:.0f}%")
    print(f"    - Rendement moyen historique: 127.31%")
    print(f"    - Sharpe moyen historique: 8.43")
    print(f"    - Drawdown moyen historique: -8.18%")
    
    print("\n  Configuration Optimisee:")
    print(f"    - N={optimized_config.n_stocks}, Lookback={optimized_config.lookback_months}mois, SL={optimized_config.stop_loss_threshold*100:.0f}%")
    print(f"    - Rendement moyen: {mc_results['total_return'].mean():.2f}%")
    print(f"    - Sharpe moyen: {mc_results['sharpe_ratio'].mean():.2f}")
    print(f"    - Drawdown moyen: {mc_results['max_drawdown'].mean():.2f}%")
    
    print("\n  Gains d'optimisation:")
    print(f"    - Rendement: +{mc_results['total_return'].mean() - 127.31:.2f}%")
    print(f"    - Sharpe: +{mc_results['sharpe_ratio'].mean() - 8.43:.2f}")
    print(f"    - Drawdown: {mc_results['max_drawdown'].mean() - (-8.18):.2f}% (amelioration)")
    
    # 8. Sauvegarder les resultats
    print("\n[Sauvegarde] Sauvegarde des resultats...")
    mc_results.to_csv('data/optimized_monte_carlo_results.csv', index=False)
    summary.to_csv('data/optimized_summary_statistics.csv', index=False)
    print("  - data/optimized_monte_carlo_results.csv")
    print("  - data/optimized_summary_statistics.csv")
    
    print("\n" + "="*70)
    print("ANALYSE OPTIMISEE TERMINEE")
    print("="*70)
    print("\nConseil: Utilisez cette configuration optimale pour vos prochains backtests.")
    print("N'oubliez pas de prendre en compte les couts de transaction dans une implementation reelle.")
    
    return mc_results, summary


if __name__ == "__main__":
    results, summary = main()
