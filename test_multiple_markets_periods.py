"""
Test de la strategie sur differents marches et periodes historiques
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from data.download_european_data import get_eurostoxx50_tickers, get_extended_period_data
from strategies.random_stoploss import RandomStopLossStrategy, StrategyConfig, run_monte_carlo_simulation


def test_single_period(prices, period_name, start_date, end_date, config, n_simulations=30):
    """
    Teste la strategie sur une periode specifique
    """
    # Filtrer les donnees pour la periode
    period_prices = prices.loc[start_date:end_date]
    
    if len(period_prices) < 100:
        print(f"  Periode trop courte: {len(period_prices)} jours")
        return None
    
    print(f"\n  Testing {period_name}: {start_date} to {end_date}")
    print(f"  Donnees disponibles: {len(period_prices)} jours, {period_prices.shape[1]} actions")
    
    # Benchmark (buy & hold equipondere)
    benchmark_returns = period_prices.pct_change().mean(axis=1)
    benchmark_total = (1 + benchmark_returns).cumprod().iloc[-1] - 1
    benchmark_cum = (1 + benchmark_returns).cumprod()
    benchmark_dd = (benchmark_cum - benchmark_cum.cummax()) / benchmark_cum.cummax()
    
    # Executer Monte Carlo
    mc_results = run_monte_carlo_simulation(
        prices=period_prices,
        n_simulations=n_simulations,
        config=config
    )
    
    if len(mc_results) == 0:
        return None
    
    result = {
        'period': period_name,
        'start': start_date,
        'end': end_date,
        'days': len(period_prices),
        'strategy_return_mean': mc_results['total_return'].mean(),
        'strategy_return_std': mc_results['total_return'].std(),
        'strategy_sharpe_mean': mc_results['sharpe_ratio'].mean(),
        'strategy_dd_mean': mc_results['max_drawdown'].mean(),
        'benchmark_return': benchmark_total * 100,
        'benchmark_max_dd': benchmark_dd.min() * 100,
        'outperformance': mc_results['total_return'].mean() - benchmark_total * 100,
        'win_rate_vs_benchmark': (mc_results['total_return'] > benchmark_total * 100).mean() * 100
    }
    
    print(f"    Strategy: {result['strategy_return_mean']:.1f}% (±{result['strategy_return_std']:.1f}%)")
    print(f"    Benchmark: {result['benchmark_return']:.1f}%")
    print(f"    Outperformance: {result['outperformance']:+.1f}%")
    print(f"    Win rate vs benchmark: {result['win_rate_vs_benchmark']:.0f}%")
    
    return result


def test_market(prices, market_name, config, periods_to_test=None):
    """
    Teste la strategie sur un marche avec differentes periodes
    """
    print(f"\n{'='*70}")
    print(f"TEST SUR {market_name}")
    print(f"{'='*70}")
    start_str = prices.index[0].strftime('%Y-%m-%d') if hasattr(prices.index[0], 'strftime') else str(prices.index[0])[:10]
    end_str = prices.index[-1].strftime('%Y-%m-%d') if hasattr(prices.index[-1], 'strftime') else str(prices.index[-1])[:10]
    print(f"Periode totale: {start_str} a {end_str}")
    print(f"Actions: {prices.shape[1]}")
    
    if periods_to_test is None:
        # Periodes par defaut
        periods_to_test = {
            'Periode Complete': (prices.index[0].strftime('%Y-%m-%d'), prices.index[-1].strftime('%Y-%m-%d')),
        }
    
    results = []
    for period_name, (start, end) in periods_to_test.items():
        result = test_single_period(prices, period_name, start, end, config, n_simulations=30)
        if result:
            results.append(result)
    
    return pd.DataFrame(results)


def compare_markets():
    """
    Compare les performances sur differents marches et periodes
    """
    print("="*70)
    print("COMPARAISON MULTI-MARCHES ET MULTI-PERIODES")
    print("="*70)
    
    # Configuration a tester
    config = StrategyConfig(
        n_stocks=20,
        lookback_months=6,
        stop_loss_threshold=-0.10,
        init_cash=100_000,
        seed=None
    )
    
    all_results = []
    
    # 1. Marche Americain - Periode recente (2018-2024)
    print("\n[1/4] Chargement des donnees US (2018-2024)...")
    try:
        us_tickers = get_sp500_tickers(100)
        us_prices = download_stock_data(us_tickers, start_date='2018-01-01', end_date='2024-12-31')
        
        us_periods = {
            'US 2018-2024 (Bull)': ('2018-01-01', '2024-12-31'),
            'US COVID Crash': ('2020-02-01', '2020-05-01'),
            'US Post-COVID': ('2020-06-01', '2021-12-31'),
            'US 2022 Bear': ('2022-01-01', '2022-12-31'),
        }
        
        us_results = test_market(us_prices, "US S&P 500", config, us_periods)
        us_results['market'] = 'US'
        all_results.append(us_results)
    except Exception as e:
        print(f"Erreur US: {e}")
    
    # 2. Marche Europeen - Periode etendue (2007-2024)
    print("\n[2/4] Chargement des donnees Europe (2007-2024)...")
    try:
        eu_tickers = get_eurostoxx50_tickers()
        # Utiliser les donnees europeennes deja telechargees
        eu_prices = pd.read_csv('data/european_prices_clean.csv', index_col=0, parse_dates=True)
        
        eu_periods = {
            'EU 2007-2024': ('2007-01-01', '2024-12-31'),
            'EU Crise 2008': ('2007-10-01', '2009-03-01'),
            'EU Dette 2010-2012': ('2010-01-01', '2012-12-31'),
            'EU COVID': ('2020-02-01', '2020-05-01'),
            'EU 2022 Energy': ('2022-01-01', '2022-12-31'),
        }
        
        eu_results = test_market(eu_prices, "Europe EURO STOXX 50", config, eu_periods)
        eu_results['market'] = 'Europe'
        all_results.append(eu_results)
    except Exception as e:
        print(f"Erreur Europe: {e}")
    
    # 3. Marche US - Periode etendue (2007-2024) pour comparaison
    print("\n[3/4] Chargement des donnees US etendues (2007-2024)...")
    try:
        # Pour US, utiliser la periode etendue disponible dans le cache
        us_prices_extended = download_stock_data(us_tickers, start_date='2018-01-01', end_date='2024-12-31')
        
        us_ext_periods = {
            'US 2007-2024': ('2007-01-01', '2024-12-31'),
            'US Crise 2008': ('2007-10-01', '2009-03-01'),
            'US Dette 2011': ('2011-05-01', '2011-12-01'),
            'US COVID': ('2020-02-01', '2020-05-01'),
        }
        
        us_ext_results = test_market(us_prices_extended, "US S&P 500 (Etendu)", config, us_ext_periods)
        us_ext_results['market'] = 'US Extended'
        all_results.append(us_ext_results)
    except Exception as e:
        print(f"Erreur US etendu: {e}")
    
    # Combiner tous les resultats
    if len(all_results) > 0:
        combined_results = pd.concat(all_results, ignore_index=True)
        combined_results.to_csv('data/multi_market_results.csv', index=False)
        
        # Afficher le tableau comparatif
        print("\n" + "="*70)
        print("TABLEAU COMPARATIF GLOBAL")
        print("="*70)
        
        pivot_return = combined_results.pivot_table(
            index='period', 
            columns='market', 
            values='strategy_return_mean'
        )
        print("\nRendement Strategie (%):")
        print(pivot_return.to_string())
        
        pivot_benchmark = combined_results.pivot_table(
            index='period', 
            columns='market', 
            values='benchmark_return'
        )
        print("\nRendement Benchmark (%):")
        print(pivot_benchmark.to_string())
        
        pivot_outperf = combined_results.pivot_table(
            index='period', 
            columns='market', 
            values='outperformance'
        )
        print("\nSurperformance vs Benchmark (pp):")
        print(pivot_outperf.to_string())
        
        # Generer visualisations
        visualize_comparison(combined_results)
        
        return combined_results
    
    return None


def visualize_comparison(results_df, save_dir='charts'):
    """
    Visualise la comparaison multi-marches
    """
    os.makedirs(save_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Comparaison Multi-Marches et Multi-Periodes', fontsize=16, fontweight='bold')
    
    # 1. Rendement Strategie vs Benchmark par periode
    ax1 = axes[0, 0]
    x = np.arange(len(results_df))
    width = 0.35
    
    ax1.bar(x - width/2, results_df['strategy_return_mean'], width, 
            label='Strategie', alpha=0.8, color='steelblue')
    ax1.bar(x + width/2, results_df['benchmark_return'], width, 
            label='Benchmark', alpha=0.8, color='coral')
    
    ax1.set_xlabel('Periode')
    ax1.set_ylabel('Rendement (%)')
    ax1.set_title('Strategie vs Benchmark par Periode')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{r['market']}\n{r['period']}" for _, r in results_df.iterrows()], 
                        rotation=45, ha='right', fontsize=8)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # 2. Surperformance
    ax2 = axes[0, 1]
    colors = ['green' if x > 0 else 'red' for x in results_df['outperformance']]
    ax2.bar(x, results_df['outperformance'], color=colors, alpha=0.7)
    ax2.set_xlabel('Periode')
    ax2.set_ylabel('Surperformance (pp)')
    ax2.set_title('Surperformance vs Benchmark')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{r['market']}\n{r['period']}" for _, r in results_df.iterrows()], 
                        rotation=45, ha='right', fontsize=8)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.grid(True, alpha=0.3)
    
    # 3. Sharpe Ratio
    ax3 = axes[1, 0]
    for market in results_df['market'].unique():
        market_data = results_df[results_df['market'] == market]
        ax3.plot(market_data['period'], market_data['strategy_sharpe_mean'], 
                marker='o', label=market, linewidth=2)
    ax3.set_xlabel('Periode')
    ax3.set_ylabel('Sharpe Ratio')
    ax3.set_title('Ratio de Sharpe par Marche')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Win Rate vs Benchmark
    ax4 = axes[1, 1]
    ax4.bar(x, results_df['win_rate_vs_benchmark'], color='forestgreen', alpha=0.7)
    ax4.set_xlabel('Periode')
    ax4.set_ylabel('Win Rate (%)')
    ax4.set_title('% de Simulations Battant le Benchmark')
    ax4.set_xticks(x)
    ax4.set_xticklabels([f"{r['market']}\n{r['period']}" for _, r in results_df.iterrows()], 
                        rotation=45, ha='right', fontsize=8)
    ax4.axhline(y=50, color='red', linestyle='--', label='50% (random)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/multi_market_comparison.png', dpi=150, bbox_inches='tight')
    print(f"\nGraphique sauvegarde: {save_dir}/multi_market_comparison.png")
    
    # 5. Tableau de synthese
    fig2, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = results_df[['market', 'period', 'strategy_return_mean', 'benchmark_return', 
                             'outperformance', 'strategy_sharpe_mean', 'win_rate_vs_benchmark']].copy()
    table_data.columns = ['Marche', 'Periode', 'Strategie (%)', 'Benchmark (%)', 
                          'Surperf (pp)', 'Sharpe', 'Win Rate (%)']
    
    table = ax.table(cellText=table_data.round(1).values,
                    colLabels=table_data.columns,
                    cellLoc='center',
                    loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Colorer les cellules de surperformance
    for i, val in enumerate(table_data['Surperf (pp)']):
        if val > 0:
            table[(i+1, 4)].set_facecolor('#90EE90')  # Vert clair
        else:
            table[(i+1, 4)].set_facecolor('#FFB6C1')  # Rose clair
    
    plt.title('Tableau Comparatif Multi-Marches', fontsize=14, fontweight='bold', pad=20)
    plt.savefig(f'{save_dir}/multi_market_table.png', dpi=150, bbox_inches='tight')
    print(f"Tableau sauvegarde: {save_dir}/multi_market_table.png")


def main():
    results = compare_markets()
    
    if results is not None:
        print("\n" + "="*70)
        print("CONCLUSIONS")
        print("="*70)
        
        # Compter les surperformances
        n_periods = len(results)
        n_surperform = (results['outperformance'] > 0).sum()
        
        print(f"\nNombre total de periodes testees: {n_periods}")
        print(f"Periodes avec surperformance: {n_surperform} ({n_surperform/n_periods*100:.0f}%)")
        print(f"Periodes avec sous-performance: {n_periods - n_surperform} ({(n_periods-n_surperform)/n_periods*100:.0f}%)")
        
        # Surperformance moyenne
        avg_outperf = results['outperformance'].mean()
        print(f"\nSurperformance moyenne: {avg_outperf:+.1f}pp")
        
        # Meilleures et pires periodes
        best = results.loc[results['outperformance'].idxmax()]
        worst = results.loc[results['outperformance'].idxmin()]
        
        print(f"\nMeilleure periode: {best['market']} - {best['period']}")
        print(f"  Surperformance: +{best['outperformance']:.1f}pp")
        
        print(f"\nPire periode: {worst['market']} - {worst['period']}")
        print(f"  Sous-performance: {worst['outperformance']:.1f}pp")
        
        print("\n" + "="*70)
    
    return results


if __name__ == "__main__":
    results = main()
