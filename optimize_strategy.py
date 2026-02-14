"""
Optimisation des hyperparametres par Grid Search
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
import itertools
import matplotlib.pyplot as plt
from tqdm import tqdm

warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from strategies.random_stoploss import RandomStopLossStrategy, StrategyConfig, run_monte_carlo_simulation


def grid_search_optimization(prices, param_grid, n_simulations_per_config=30):
    """
    Grid search pour trouver les meilleurs hyperparametres
    
    Args:
        prices: DataFrame des prix historiques
        param_grid: Dictionnaire des parametres a tester
        n_simulations_per_config: Nombre de simulations Monte Carlo par configuration
    
    Returns:
        DataFrame avec les resultats de chaque configuration
    """
    
    # Generer toutes les combinaisons de parametres
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    all_combinations = list(itertools.product(*param_values))
    
    print(f"Grid Search: {len(all_combinations)} configurations a tester")
    print(f"Simulations par config: {n_simulations_per_config}")
    print(f"Total simulations: {len(all_combinations) * n_simulations_per_config}")
    print("=" * 70)
    
    results = []
    
    for i, combo in enumerate(all_combinations):
        params = dict(zip(param_names, combo))
        
        print(f"\n[{i+1}/{len(all_combinations)}] Test: n_stocks={params['n_stocks']}, "
              f"lookback={params['lookback_months']}mois, "
              f"stop_loss={params['stop_loss_threshold']*100:.0f}%")
        
        # Creer la config
        config = StrategyConfig(
            n_stocks=params['n_stocks'],
            lookback_months=params['lookback_months'],
            stop_loss_threshold=params['stop_loss_threshold'],
            init_cash=100_000,
            seed=None
        )
        
        # Executer les simulations Monte Carlo
        mc_results = run_monte_carlo_simulation(
            prices=prices,
            n_simulations=n_simulations_per_config,
            config=config
        )
        
        if len(mc_results) > 0:
            # Calculer les metriques agregees
            result = {
                'n_stocks': params['n_stocks'],
                'lookback_months': params['lookback_months'],
                'stop_loss_threshold': params['stop_loss_threshold'],
                'mean_return': mc_results['total_return'].mean(),
                'std_return': mc_results['total_return'].std(),
                'min_return': mc_results['total_return'].min(),
                'max_return': mc_results['total_return'].max(),
                'median_return': mc_results['total_return'].median(),
                'mean_sharpe': mc_results['sharpe_ratio'].mean(),
                'std_sharpe': mc_results['sharpe_ratio'].std(),
                'mean_drawdown': mc_results['max_drawdown'].mean(),
                'std_drawdown': mc_results['max_drawdown'].std(),
                'win_rate': (mc_results['total_return'] > 0).mean() * 100,
                'risk_adjusted_return': mc_results['total_return'].mean() / abs(mc_results['max_drawdown'].mean()),
                'sharpe_of_returns': mc_results['total_return'].mean() / mc_results['total_return'].std() if mc_results['total_return'].std() > 0 else 0,
                'n_simulations': len(mc_results)
            }
            results.append(result)
            
            print(f"  -> Rendement: {result['mean_return']:.1f}% (±{result['std_return']:.1f}%), "
                  f"Sharpe: {result['mean_sharpe']:.2f}, "
                  f"Drawdown: {result['mean_drawdown']:.1f}%")
    
    return pd.DataFrame(results)


def find_optimal_config(results_df, objective='sharpe'):
    """
    Trouve la configuration optimale selon differents criteres
    
    Args:
        results_df: DataFrame avec les resultats du grid search
        objective: 'sharpe', 'return', 'risk_adjusted', ou 'balanced'
    
    Returns:
        Series avec la meilleure configuration
    """
    
    if objective == 'sharpe':
        # Maximiser le ratio de Sharpe
        best_idx = results_df['mean_sharpe'].idxmax()
        criteria = "Ratio de Sharpe"
        
    elif objective == 'return':
        # Maximiser le rendement
        best_idx = results_df['mean_return'].idxmax()
        criteria = "Rendement total"
        
    elif objective == 'risk_adjusted':
        # Maximiser le rendement ajuste au risque (return / |drawdown|)
        best_idx = results_df['risk_adjusted_return'].idxmax()
        criteria = "Rendement ajuste au risque"
        
    elif objective == 'balanced':
        # Score combine: normaliser et combiner sharpe et rendement
        results_df['sharpe_norm'] = (results_df['mean_sharpe'] - results_df['mean_sharpe'].min()) / \
                                     (results_df['mean_sharpe'].max() - results_df['mean_sharpe'].min())
        results_df['return_norm'] = (results_df['mean_return'] - results_df['mean_return'].min()) / \
                                     (results_df['mean_return'].max() - results_df['mean_return'].min())
        results_df['balanced_score'] = 0.5 * results_df['sharpe_norm'] + 0.5 * results_df['return_norm']
        best_idx = results_df['balanced_score'].idxmax()
        criteria = "Score equilibre (Sharpe + Rendement)"
        
    else:
        raise ValueError(f"Objectif inconnu: {objective}")
    
    best_config = results_df.loc[best_idx]
    
    print(f"\n{'='*70}")
    print(f"CONFIGURATION OPTIMALE (critere: {criteria})")
    print(f"{'='*70}")
    print(f"  Nombre d'actions:        {int(best_config['n_stocks'])}")
    print(f"  Lookback (mois):         {int(best_config['lookback_months'])}")
    print(f"  Seuil stop-loss:         {best_config['stop_loss_threshold']*100:.0f}%")
    print(f"\n  Performance:")
    print(f"    - Rendement moyen:     {best_config['mean_return']:.2f}%")
    print(f"    - Ratio de Sharpe:     {best_config['mean_sharpe']:.2f}")
    print(f"    - Max Drawdown:        {best_config['mean_drawdown']:.2f}%")
    print(f"    - Win rate:            {best_config['win_rate']:.1f}%")
    print(f"{'='*70}")
    
    return best_config


def visualize_optimization_results(results_df, save_dir='charts'):
    """
    Visualise les resultats de l'optimisation
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Heatmap: Rendement vs Parametres
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Optimisation des Hyperparametres - Grid Search', fontsize=14, fontweight='bold')
    
    # Rendement moyen
    ax1 = axes[0, 0]
    pivot_return = results_df.pivot_table(
        values='mean_return', 
        index='lookback_months', 
        columns='stop_loss_threshold'
    )
    im1 = ax1.imshow(pivot_return.values, cmap='RdYlGn', aspect='auto')
    ax1.set_xticks(range(len(pivot_return.columns)))
    ax1.set_xticklabels([f"{x*100:.0f}%" for x in pivot_return.columns])
    ax1.set_yticks(range(len(pivot_return.index)))
    ax1.set_yticklabels(pivot_return.index)
    ax1.set_xlabel('Seuil Stop-Loss')
    ax1.set_ylabel('Lookback (mois)')
    ax1.set_title('Rendement Moyen (%)')
    plt.colorbar(im1, ax=ax1)
    
    # Ratio de Sharpe
    ax2 = axes[0, 1]
    pivot_sharpe = results_df.pivot_table(
        values='mean_sharpe', 
        index='lookback_months', 
        columns='stop_loss_threshold'
    )
    im2 = ax2.imshow(pivot_sharpe.values, cmap='RdYlGn', aspect='auto')
    ax2.set_xticks(range(len(pivot_sharpe.columns)))
    ax2.set_xticklabels([f"{x*100:.0f}%" for x in pivot_sharpe.columns])
    ax2.set_yticks(range(len(pivot_sharpe.index)))
    ax2.set_yticklabels(pivot_sharpe.index)
    ax2.set_xlabel('Seuil Stop-Loss')
    ax2.set_ylabel('Lookback (mois)')
    ax2.set_title('Ratio de Sharpe Moyen')
    plt.colorbar(im2, ax=ax2)
    
    # Max Drawdown
    ax3 = axes[1, 0]
    pivot_dd = results_df.pivot_table(
        values='mean_drawdown', 
        index='lookback_months', 
        columns='stop_loss_threshold'
    )
    im3 = ax3.imshow(pivot_dd.values, cmap='RdYlGn_r', aspect='auto')  # _r pour inverser (rouge = mauvais)
    ax3.set_xticks(range(len(pivot_dd.columns)))
    ax3.set_xticklabels([f"{x*100:.0f}%" for x in pivot_dd.columns])
    ax3.set_yticks(range(len(pivot_dd.index)))
    ax3.set_yticklabels(pivot_dd.index)
    ax3.set_xlabel('Seuil Stop-Loss')
    ax3.set_ylabel('Lookback (mois)')
    ax3.set_title('Max Drawdown Moyen (%)')
    plt.colorbar(im3, ax=ax3)
    
    # Rendement ajuste au risque
    ax4 = axes[1, 1]
    pivot_risk_adj = results_df.pivot_table(
        values='risk_adjusted_return', 
        index='lookback_months', 
        columns='stop_loss_threshold'
    )
    im4 = ax4.imshow(pivot_risk_adj.values, cmap='RdYlGn', aspect='auto')
    ax4.set_xticks(range(len(pivot_risk_adj.columns)))
    ax4.set_xticklabels([f"{x*100:.0f}%" for x in pivot_risk_adj.columns])
    ax4.set_yticks(range(len(pivot_risk_adj.index)))
    ax4.set_yticklabels(pivot_risk_adj.index)
    ax4.set_xlabel('Seuil Stop-Loss')
    ax4.set_ylabel('Lookback (mois)')
    ax4.set_title('Rendement Ajuste au Risque')
    plt.colorbar(im4, ax=ax4)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/optimization_heatmaps.png', dpi=150, bbox_inches='tight')
    print(f"\nGraphique sauvegarde: {save_dir}/optimization_heatmaps.png")
    
    # 2. Graphique 3D de la surface de reponse
    fig2 = plt.figure(figsize=(14, 5))
    
    # Rendement vs N Stocks et Stop-Loss
    ax1_3d = fig2.add_subplot(131, projection='3d')
    for n in results_df['n_stocks'].unique():
        subset = results_df[results_df['n_stocks'] == n]
        ax1_3d.scatter(subset['stop_loss_threshold'] * 100, 
                       subset['lookback_months'], 
                       subset['mean_return'], 
                       label=f'{int(n)} actions', s=50, alpha=0.7)
    ax1_3d.set_xlabel('Stop-Loss (%)')
    ax1_3d.set_ylabel('Lookback (mois)')
    ax1_3d.set_zlabel('Rendement (%)')
    ax1_3d.set_title('Rendement Moyen')
    ax1_3d.legend()
    
    # Sharpe vs N Stocks et Stop-Loss
    ax2_3d = fig2.add_subplot(132, projection='3d')
    for n in results_df['n_stocks'].unique():
        subset = results_df[results_df['n_stocks'] == n]
        ax2_3d.scatter(subset['stop_loss_threshold'] * 100, 
                       subset['lookback_months'], 
                       subset['mean_sharpe'], 
                       label=f'{int(n)} actions', s=50, alpha=0.7)
    ax2_3d.set_xlabel('Stop-Loss (%)')
    ax2_3d.set_ylabel('Lookback (mois)')
    ax2_3d.set_zlabel('Sharpe')
    ax2_3d.set_title('Ratio de Sharpe')
    ax2_3d.legend()
    
    # Drawdown vs N Stocks et Stop-Loss
    ax3_3d = fig2.add_subplot(133, projection='3d')
    for n in results_df['n_stocks'].unique():
        subset = results_df[results_df['n_stocks'] == n]
        ax3_3d.scatter(subset['stop_loss_threshold'] * 100, 
                       subset['lookback_months'], 
                       subset['mean_drawdown'], 
                       label=f'{int(n)} actions', s=50, alpha=0.7)
    ax3_3d.set_xlabel('Stop-Loss (%)')
    ax3_3d.set_ylabel('Lookback (mois)')
    ax3_3d.set_zlabel('Drawdown (%)')
    ax3_3d.set_title('Max Drawdown')
    ax3_3d.legend()
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/optimization_3d.png', dpi=150, bbox_inches='tight')
    print(f"Graphique sauvegarde: {save_dir}/optimization_3d.png")
    
    # 3. Top 10 configurations
    fig3, axes3 = plt.subplots(1, 2, figsize=(14, 6))
    fig3.suptitle('Top 10 Configurations par Criteres', fontsize=14, fontweight='bold')
    
    # Top 10 Sharpe
    ax_top1 = axes3[0]
    top_sharpe = results_df.nlargest(10, 'mean_sharpe')
    labels = [f"N{int(row['n_stocks'])}/L{int(row['lookback_months'])}/SL{row['stop_loss_threshold']*100:.0f}%" 
              for _, row in top_sharpe.iterrows()]
    ax_top1.barh(range(len(top_sharpe)), top_sharpe['mean_sharpe'], color='forestgreen', alpha=0.7)
    ax_top1.set_yticks(range(len(top_sharpe)))
    ax_top1.set_yticklabels(labels, fontsize=8)
    ax_top1.set_xlabel('Ratio de Sharpe')
    ax_top1.set_title('Top 10 - Ratio de Sharpe')
    ax_top1.invert_yaxis()
    ax_top1.grid(True, alpha=0.3)
    
    # Top 10 Rendement
    ax_top2 = axes3[1]
    top_return = results_df.nlargest(10, 'mean_return')
    labels = [f"N{int(row['n_stocks'])}/L{int(row['lookback_months'])}/SL{row['stop_loss_threshold']*100:.0f}%" 
              for _, row in top_return.iterrows()]
    ax_top2.barh(range(len(top_return)), top_return['mean_return'], color='steelblue', alpha=0.7)
    ax_top2.set_yticks(range(len(top_return)))
    ax_top2.set_yticklabels(labels, fontsize=8)
    ax_top2.set_xlabel('Rendement Moyen (%)')
    ax_top2.set_title('Top 10 - Rendement')
    ax_top2.invert_yaxis()
    ax_top2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/optimization_top10.png', dpi=150, bbox_inches='tight')
    print(f"Graphique sauvegarde: {save_dir}/optimization_top10.png")


def compare_configs(prices, baseline_config, optimized_config, n_simulations=50):
    """
    Compare la configuration de base avec l'optimisee
    """
    print("\n" + "="*70)
    print("COMPARAISON: CONFIGURATION DE BASE vs OPTIMISEE")
    print("="*70)
    
    # Test configuration de base
    print("\n1. Configuration DE BASE:")
    print(f"   n_stocks={baseline_config.n_stocks}, "
          f"lookback={baseline_config.lookback_months}mois, "
          f"stop_loss={baseline_config.stop_loss_threshold*100:.0f}%")
    
    baseline_results = run_monte_carlo_simulation(prices, n_simulations, baseline_config)
    
    # Test configuration optimale
    print("\n2. Configuration OPTIMISEE:")
    print(f"   n_stocks={optimized_config.n_stocks}, "
          f"lookback={optimized_config.lookback_months}mois, "
          f"stop_loss={optimized_config.stop_loss_threshold*100:.0f}%")
    
    optimized_results = run_monte_carlo_simulation(prices, n_simulations, optimized_config)
    
    # Comparaison
    print("\n" + "="*70)
    print("RESULTATS COMPARES")
    print("="*70)
    
    comparison = pd.DataFrame({
        'Metrique': ['Rendement Moyen (%)', 'Rendement Median (%)', 'Sharpe Moyen', 
                     'Sharpe Median', 'Drawdown Moyen (%)', 'Win Rate (%)'],
        'Configuration de Base': [
            baseline_results['total_return'].mean(),
            baseline_results['total_return'].median(),
            baseline_results['sharpe_ratio'].mean(),
            baseline_results['sharpe_ratio'].median(),
            baseline_results['max_drawdown'].mean(),
            (baseline_results['total_return'] > 0).mean() * 100
        ],
        'Configuration Optimisee': [
            optimized_results['total_return'].mean(),
            optimized_results['total_return'].median(),
            optimized_results['sharpe_ratio'].mean(),
            optimized_results['sharpe_ratio'].median(),
            optimized_results['max_drawdown'].mean(),
            (optimized_results['total_return'] > 0).mean() * 100
        ]
    })
    
    comparison['Difference'] = comparison['Configuration Optimisee'] - comparison['Configuration de Base']
    comparison['Amelioration (%)'] = (comparison['Difference'] / comparison['Configuration de Base'] * 100).abs()
    
    print(comparison.to_string(index=False))
    
    # Sauvegarder la comparaison
    comparison.to_csv('data/comparison_baseline_optimized.csv', index=False)
    print("\nComparaison sauvegardee: data/comparison_baseline_optimized.csv")
    
    return comparison


def main():
    print("="*70)
    print("OPTIMISATION DES HYPERPARAMETRES - GRID SEARCH")
    print("="*70)
    
    # 1. Charger les donnees
    print("\n[ETAPE 1] Chargement des donnees")
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    print(f"Donnees chargees: {prices.shape[1]} actions, {prices.shape[0]} jours")
    
    # 2. Definir la grille de parametres (restreinte pour la rapidite)
    print("\n[ETAPE 2] Configuration du Grid Search")
    
    param_grid = {
        'n_stocks': [10, 15, 20, 25, 30],           # Diversification
        'lookback_months': [3, 6, 9, 12],           # Periode d'evaluation
        'stop_loss_threshold': [-0.05, -0.10, -0.15, -0.20]  # Seuil de sortie
    }
    
    print(f"Parametres testes:")
    for key, values in param_grid.items():
        print(f"  {key}: {values}")
    
    # 3. Executer le grid search
    print("\n[ETAPE 3] Execution du Grid Search")
    results_df = grid_search_optimization(
        prices=prices,
        param_grid=param_grid,
        n_simulations_per_config=20  # Reduit pour la rapidite
    )
    
    # 4. Sauvegarder les resultats
    results_df.to_csv('data/grid_search_results.csv', index=False)
    print(f"\nResultats sauvegardes: data/grid_search_results.csv")
    
    # 5. Trouver les configurations optimales selon differents criteres
    print("\n[ETAPE 4] Analyse des Resultats")
    
    print("\n" + "-"*70)
    best_sharpe = find_optimal_config(results_df, objective='sharpe')
    
    print("\n" + "-"*70)
    best_return = find_optimal_config(results_df, objective='return')
    
    print("\n" + "-"*70)
    best_risk_adj = find_optimal_config(results_df, objective='risk_adjusted')
    
    print("\n" + "-"*70)
    best_balanced = find_optimal_config(results_df, objective='balanced')
    
    # 6. Visualiser
    print("\n[ETAPE 5] Generation des Visualisations")
    visualize_optimization_results(results_df)
    
    # 7. Comparer avec la configuration initiale
    print("\n[ETAPE 6] Comparaison avec Configuration de Base")
    
    baseline_config = StrategyConfig(
        n_stocks=20,
        lookback_months=6,
        stop_loss_threshold=-0.10,
        init_cash=100_000,
        seed=42
    )
    
    # Utiliser la config optimale selon Sharpe pour la comparaison
    optimized_config = StrategyConfig(
        n_stocks=int(best_sharpe['n_stocks']),
        lookback_months=int(best_sharpe['lookback_months']),
        stop_loss_threshold=best_sharpe['stop_loss_threshold'],
        init_cash=100_000,
        seed=42
    )
    
    comparison = compare_configs(prices, baseline_config, optimized_config, n_simulations=30)
    
    print("\n" + "="*70)
    print("OPTIMISATION TERMINEE")
    print("="*70)
    
    return results_df, best_sharpe, best_return, best_risk_adj, best_balanced


if __name__ == "__main__":
    results, best_s, best_r, best_ra, best_b = main()
