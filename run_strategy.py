"""
Script principal pour tester la stratégie de sélection aléatoire avec stop-loss
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
    print("=" * 70)
    print("STRATÉGIE DE SÉLECTION ALÉATOIRE AVEC STOP-LOSS")
    print("=" * 70)
    print("\nDescription:")
    print("- Sélection aléatoire de 20 actions")
    print("- Rebalancement mensuel")
    print("- Règle d'éviction: si performance 6 mois < -10%, remplacer l'action")
    print("- Simulations Monte Carlo pour évaluer la robustesse")
    print("=" * 70)
    
    # 1. Télécharger les données
    print("\n[ETAPE 1] Telechargement des donnees")
    tickers = get_sp500_tickers(100)  # Top 100 S&P 500
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    
    print(f"\nPériode analysée: {prices.index[0].strftime('%Y-%m-%d')} à {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Nombre d'actions disponibles: {prices.shape[1]}")
    print(f"Nombre de jours de trading: {prices.shape[0]}")
    
    # 2. Configuration de la stratégie
    print("\n[ETAPE 2] Configuration de la strategie")
    config = StrategyConfig(
        n_stocks=20,
        lookback_months=6,
        stop_loss_threshold=-0.10,
        init_cash=100_000,
        seed=42
    )
    print(f"  - Nombre d'actions: {config.n_stocks}")
    print(f"  - Lookback stop-loss: {config.lookback_months} mois")
    print(f"  - Seuil stop-loss: {config.stop_loss_threshold * 100:.0f}%")
    print(f"  - Capital initial: ${config.init_cash:,.0f}")
    
    # 3. Test individuel
    print("\n[ETAPE 3] Test d'une simulation individuelle")
    strategy = RandomStopLossStrategy(config)
    result = strategy.run_backtest_simple(prices, verbose=True)
    
    if result:
        print(f"\n  Résultats de la simulation:")
        print(f"    - Rendement total: {result['total_return']:.2f}%")
        print(f"    - Ratio de Sharpe: {result['sharpe_ratio']:.2f}")
        print(f"    - Max Drawdown: {result['max_drawdown']:.2f}%")
        print(f"    - Valeur finale: ${result['final_value']:,.2f}")
    
    # 4. Simulations Monte Carlo
    print("\n[ETAPE 4] Simulations Monte Carlo (50 simulations)")
    mc_results = run_monte_carlo_simulation(
        prices=prices,
        n_simulations=50,
        config=config
    )
    
    # 5. Analyse des résultats
    print("\n[ETAPE 5] Analyse statistique")
    print("\n" + "=" * 70)
    print("RÉSULTATS DES SIMULATIONS MONTE CARLO (n=50)")
    print("=" * 70)
    
    metrics = ['total_return', 'sharpe_ratio', 'max_drawdown', 
               'annualized_return', 'annualized_volatility', 'calmar_ratio']
    
    summary = pd.DataFrame({
        'Métrique': [],
        'Moyenne': [],
        'Médiane': [],
        'Écart-type': [],
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
                    'Métrique': [metric],
                    'Moyenne': [values.mean()],
                    'Médiane': [values.median()],
                    'Écart-type': [values.std()],
                    'Min': [values.min()],
                    'Max': [values.max()],
                    'Percentile 5%': [values.quantile(0.05)],
                    'Percentile 95%': [values.quantile(0.95)]
                })], ignore_index=True)
    
    print("\n", summary.to_string(index=False))
    
    # 6. Comparaison avec le benchmark (Buy & Hold S&P 500)
    print("\n" + "=" * 70)
    print("COMPARAISON AVEC BENCHMARK (Buy & Hold S&P 500)")
    print("=" * 70)
    
    # Simuler un portefeuille équipondéré de toutes les actions comme benchmark
    benchmark_returns = prices.pct_change().mean(axis=1)  # Moyenne de toutes les actions
    benchmark_cum = (1 + benchmark_returns).cumprod()
    benchmark_total_return = (benchmark_cum.iloc[-1] - 1) * 100
    
    print(f"\n  Benchmark (Buy & Hold équipondéré):")
    print(f"    - Rendement total: {benchmark_total_return:.2f}%")
    
    print(f"\n  Stratégie Random + Stop-Loss (moyenne Monte Carlo):")
    print(f"    - Rendement total moyen: {mc_results['total_return'].mean():.2f}%")
    print(f"    - Ratio de Sharpe moyen: {mc_results['sharpe_ratio'].mean():.2f}")
    print(f"    - Max Drawdown moyen: {mc_results['max_drawdown'].mean():.2f}%")
    
    outperformance = mc_results['total_return'].mean() - benchmark_total_return
    print(f"\n  Surperformance vs Benchmark: {outperformance:.2f}%")
    
    # 7. Distribution des résultats
    print("\n" + "=" * 70)
    print("DISTRIBUTION DES RENDEMENTS")
    print("=" * 70)
    returns = mc_results['total_return'].dropna()
    
    print(f"\n  Nombre de simulations: {len(returns)}")
    print(f"  Simulations positives: {(returns > 0).sum()} ({(returns > 0).mean() * 100:.1f}%)")
    print(f"  Simulations > Benchmark: {(returns > benchmark_total_return).sum()} ({(returns > benchmark_total_return).mean() * 100:.1f}%)")
    print(f"  Simulations > 50%: {(returns > 50).sum()} ({(returns > 50).mean() * 100:.1f}%)")
    print(f"  Simulations < -20%: {(returns < -20).sum()} ({(returns < -20).mean() * 100:.1f}%)")
    
    # 8. Sauvegarder les résultats
    print("\n[Sauvegarde] Sauvegarde des resultats...")
    mc_results.to_csv('data/monte_carlo_results.csv', index=False)
    summary.to_csv('data/summary_statistics.csv', index=False)
    print("  - data/monte_carlo_results.csv")
    print("  - data/summary_statistics.csv")
    
    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE")
    print("=" * 70)
    
    return mc_results, summary


if __name__ == "__main__":
    results, summary = main()
