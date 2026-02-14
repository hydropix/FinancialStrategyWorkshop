"""
Analyse de l'impact des frais de transaction sur la strategie Random + Stop-Loss
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
from strategies.random_stoploss import StrategyConfig


class TransactionCostAnalyzer:
    """Analyse l'impact des couts de transaction"""
    
    def __init__(self, config, transaction_cost_pct=0.001):
        """
        Args:
            transaction_cost_pct: Cout par transaction (0.001 = 0.1%)
        """
        self.config = config
        self.transaction_cost_pct = transaction_cost_pct
        
    def run_backtest_with_costs(self, prices, verbose=False):
        """
        Backtest avec prise en compte des frais de transaction
        """
        all_stocks = prices.columns.tolist()
        lookback_days = self.config.lookback_months * 21
        n_stocks = self.config.n_stocks
        init_cash = self.config.init_cash
        
        # Dates de rebalancement
        rebalance_dates = pd.date_range(start=prices.index[0], 
                                       end=prices.index[-1], 
                                       freq='MS')
        rebalance_dates = prices.index[prices.index.isin(rebalance_dates)]
        
        if len(rebalance_dates) < 2:
            rebalance_dates = prices.index[::21]
        
        # Suivi des transactions
        transactions_count = 0
        buy_volume = 0
        sell_volume = 0
        total_fees = 0
        
        # Initialisation
        current_portfolio = np.random.choice(all_stocks, size=n_stocks, replace=False).tolist()
        cash = init_cash
        holdings = {stock: 0 for stock in all_stocks}
        portfolio_values = []
        portfolio_history = []
        
        for i, date in enumerate(rebalance_dates):
            if date not in prices.index:
                continue
                
            current_prices = prices.loc[date]
            
            # Valeur avant rebalancement
            portfolio_value_before = cash
            for stock, qty in holdings.items():
                if qty > 0 and stock in current_prices.index:
                    portfolio_value_before += qty * current_prices[stock]
            
            actions_sold = []
            actions_bought = []
            
            if i == 0:
                # Premier achat
                allocation_per_stock = init_cash / n_stocks
                for stock in current_portfolio:
                    if stock in current_prices.index and current_prices[stock] > 0:
                        qty = int(allocation_per_stock / current_prices[stock])
                        if qty > 0:
                            cost = qty * current_prices[stock]
                            fee = cost * self.transaction_cost_pct
                            holdings[stock] = qty
                            cash -= (cost + fee)
                            buy_volume += cost
                            total_fees += fee
                            transactions_count += 1
                            actions_bought.append(stock)
            else:
                # Verifier les actions a evincer
                hist_prices = prices.loc[:date]
                
                if len(hist_prices) >= lookback_days:
                    # Calculer les performances
                    recent_prices = hist_prices.iloc[-lookback_days:]
                    performances = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]
                    
                    stocks_to_evict = []
                    for stock in current_portfolio:
                        if stock in performances.index:
                            if performances[stock] < self.config.stop_loss_threshold:
                                stocks_to_evict.append(stock)
                    
                    if len(stocks_to_evict) > 0:
                        # Vendre les actions evincees
                        for stock in stocks_to_evict:
                            if holdings[stock] > 0 and stock in current_prices.index:
                                sale_value = holdings[stock] * current_prices[stock]
                                fee = sale_value * self.transaction_cost_pct
                                cash += (sale_value - fee)
                                sell_volume += sale_value
                                total_fees += fee
                                holdings[stock] = 0
                                transactions_count += 1
                                actions_sold.append(stock)
                        
                        # Acheter de nouvelles actions
                        available = [s for s in all_stocks if s not in current_portfolio]
                        n_to_add = len(stocks_to_evict)
                        
                        if len(available) >= n_to_add and n_to_add > 0:
                            new_stocks = np.random.choice(available, size=n_to_add, replace=False).tolist()
                            
                            # Mettre a jour le portefeuille
                            for old_stock in stocks_to_evict:
                                current_portfolio.remove(old_stock)
                            current_portfolio.extend(new_stocks)
                            
                            # Acheter
                            allocation_per_stock = cash / n_to_add
                            for stock in new_stocks:
                                if stock in current_prices.index and current_prices[stock] > 0:
                                    qty = int(allocation_per_stock / current_prices[stock])
                                    if qty > 0:
                                        cost = qty * current_prices[stock]
                                        fee = cost * self.transaction_cost_pct
                                        holdings[stock] = qty
                                        cash -= (cost + fee)
                                        buy_volume += cost
                                        total_fees += fee
                                        transactions_count += 1
                                        actions_bought.append(stock)
            
            # Valeur apres rebalancement
            portfolio_value_after = cash
            for stock, qty in holdings.items():
                if qty > 0 and stock in current_prices.index:
                    portfolio_value_after += qty * current_prices[stock]
            
            portfolio_values.append({
                'date': date, 
                'value': portfolio_value_after,
                'value_no_fees': portfolio_value_before
            })
            
            portfolio_history.append({
                'date': date,
                'portfolio': current_portfolio.copy(),
                'actions_sold': actions_sold,
                'actions_bought': actions_bought,
                'n_transactions': len(actions_sold) + len(actions_bought)
            })
        
        # Calculer les metriques
        final_value = portfolio_values[-1]['value'] if portfolio_values else init_cash
        final_value_no_fees = portfolio_values[-1]['value_no_fees'] if portfolio_values else init_cash
        
        total_return = (final_value - init_cash) / init_cash * 100
        total_return_no_fees = (final_value_no_fees - init_cash) / init_cash * 100
        
        # Calculer le Sharpe
        values_df = pd.DataFrame(portfolio_values).set_index('date')
        returns = values_df['value'].pct_change().dropna()
        
        if len(returns) > 1 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
            cummax = values_df['value'].cummax()
            drawdown = (values_df['value'] - cummax) / cummax
            max_drawdown = drawdown.min() * 100
        else:
            sharpe_ratio = 0
            max_drawdown = 0
        
        return {
            'total_return': total_return,
            'total_return_no_fees': total_return_no_fees,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': final_value,
            'final_value_no_fees': final_value_no_fees,
            'total_fees': total_fees,
            'transactions_count': transactions_count,
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'portfolio_values': portfolio_values,
            'portfolio_history': portfolio_history,
            'impact_fees_pct': total_return_no_fees - total_return
        }


def run_monte_carlo_with_costs(prices, config, n_simulations=50, transaction_cost_pct=0.001):
    """
    Monte Carlo avec frais de transaction
    """
    results = []
    
    print(f"Simulations avec frais de {transaction_cost_pct*100:.2f}% par transaction...")
    
    for i in range(n_simulations):
        if (i + 1) % 10 == 0:
            print(f"  Simulation {i + 1}/{n_simulations}")
        
        sim_config = StrategyConfig(
            n_stocks=config.n_stocks,
            lookback_months=config.lookback_months,
            stop_loss_threshold=config.stop_loss_threshold,
            init_cash=100_000,
            seed=i
        )
        
        analyzer = TransactionCostAnalyzer(sim_config, transaction_cost_pct)
        result = analyzer.run_backtest_with_costs(prices, verbose=False)
        
        if result:
            results.append({
                'simulation': i + 1,
                'seed': i,
                'total_return': result['total_return'],
                'total_return_no_fees': result['total_return_no_fees'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'total_fees': result['total_fees'],
                'transactions_count': result['transactions_count'],
                'impact_fees_pct': result['impact_fees_pct'],
                'final_value': result['final_value'],
                'final_value_no_fees': result['final_value_no_fees']
            })
    
    return pd.DataFrame(results)


def main():
    print("="*70)
    print("ANALYSE DE L'IMPACT DES FRAIS DE TRANSACTION")
    print("="*70)
    
    # 1. Charger les donnees
    print("\n[ETAPE 1] Chargement des donnees")
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01', end_date='2024-12-31')
    
    # 2. Configurations a tester
    configs = {
        'BASE (20/6/-10%)': StrategyConfig(n_stocks=20, lookback_months=6, stop_loss_threshold=-0.10, init_cash=100_000),
        'OPTIMISEE (30/3/-5%)': StrategyConfig(n_stocks=30, lookback_months=3, stop_loss_threshold=-0.05, init_cash=100_000),
    }
    
    # 3. Niveaux de frais a tester
    fee_levels = [
        ('0.00%', 0.0),
        ('0.10%', 0.001),
        ('0.20%', 0.002),
        ('0.50%', 0.005),
        ('1.00%', 0.01),
    ]
    
    # 4. Analyse pour chaque configuration et niveau de frais
    all_results = []
    
    for config_name, config in configs.items():
        print(f"\n{'='*70}")
        print(f"Configuration: {config_name}")
        print(f"{'='*70}")
        
        for fee_label, fee_pct in fee_levels:
            print(f"\n  Frais: {fee_label}")
            
            mc_results = run_monte_carlo_with_costs(
                prices=prices,
                config=config,
                n_simulations=30,
                transaction_cost_pct=fee_pct
            )
            
            result_summary = {
                'config': config_name,
                'fee_label': fee_label,
                'fee_pct': fee_pct,
                'mean_return': mc_results['total_return'].mean(),
                'mean_return_no_fees': mc_results['total_return_no_fees'].mean(),
                'mean_sharpe': mc_results['sharpe_ratio'].mean(),
                'mean_drawdown': mc_results['max_drawdown'].mean(),
                'mean_fees': mc_results['total_fees'].mean(),
                'mean_transactions': mc_results['transactions_count'].mean(),
                'impact_fees': mc_results['impact_fees_pct'].mean(),
                'final_value': mc_results['final_value'].mean(),
                'final_value_no_fees': mc_results['final_value_no_fees'].mean()
            }
            
            all_results.append(result_summary)
            
            print(f"    Rendement: {result_summary['mean_return']:.1f}% "
                  f"(vs {result_summary['mean_return_no_fees']:.1f}% sans frais)")
            print(f"    Frais totaux moyens: ${result_summary['mean_fees']:,.0f}")
            print(f"    Transactions moyennes: {result_summary['mean_transactions']:.0f}")
            print(f"    Impact des frais: -{result_summary['impact_fees']:.1f}pp")
    
    # 5. Creer DataFrame de synthese
    results_df = pd.DataFrame(all_results)
    results_df.to_csv('data/transaction_costs_analysis.csv', index=False)
    
    # 6. Visualisation
    print("\n[ETAPE 2] Generation des visualisations")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Impact des Frais de Transaction sur les Performances', fontsize=14, fontweight='bold')
    
    for config_name in configs.keys():
        config_data = results_df[results_df['config'] == config_name]
        
        # Graphique 1: Rendement vs Frais
        ax1 = axes[0, 0]
        ax1.plot(config_data['fee_pct'] * 100, config_data['mean_return'], 
                marker='o', linewidth=2, label=config_name)
        ax1.set_xlabel('Frais de Transaction (%)')
        ax1.set_ylabel('Rendement Moyen (%)')
        ax1.set_title('Impact des Frais sur le Rendement')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Graphique 2: Perte due aux frais
        ax2 = axes[0, 1]
        ax2.bar(config_data['fee_label'], config_data['impact_fees'], 
                alpha=0.7, label=config_name)
        ax2.set_xlabel('Niveau de Frais')
        ax2.set_ylabel('Perte de Performance (pp)')
        ax2.set_title('Perte de Performance due aux Frais')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Graphique 3: Nombre de transactions
        ax3 = axes[1, 0]
        ax3.plot(config_data['fee_pct'] * 100, config_data['mean_transactions'], 
                marker='s', linewidth=2, label=config_name)
        ax3.set_xlabel('Frais de Transaction (%)')
        ax3.set_ylabel('Nombre moyen de transactions')
        ax3.set_title('Volume de Transactions')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Graphique 4: Frais totaux payes
        ax4 = axes[1, 1]
        ax4.plot(config_data['fee_pct'] * 100, config_data['mean_fees'], 
                marker='^', linewidth=2, label=config_name)
        ax4.set_xlabel('Frais de Transaction (%)')
        ax4.set_ylabel('Frais totaux moyens ($)')
        ax4.set_title('Cout Total des Transactions')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('charts/transaction_costs_impact.png', dpi=150, bbox_inches='tight')
    print("  Sauvegarde: charts/transaction_costs_impact.png")
    
    # 7. Analyse de la surperformance
    print("\n" + "="*70)
    print("ANALYSE DE LA SURPERFORMANCE VS BENCHMARK")
    print("="*70)
    
    benchmark_return = 190.86  # S&P 500 equipondere
    
    for config_name in configs.keys():
        print(f"\n{config_name}:")
        config_data = results_df[results_df['config'] == config_name]
        
        for _, row in config_data.iterrows():
            outperformance = row['mean_return'] - benchmark_return
            status = "[SURPERFORME]" if outperformance > 0 else "[SOUS-PERFORME]"
            print(f"  {row['fee_label']:>6} -> Rendement: {row['mean_return']:>6.1f}% "
                  f"vs Benchmark: {benchmark_return:.1f}% "
                  f"({outperformance:+.1f}%) {status}")
    
    # 8. Seuil critique de frais
    print("\n" + "="*70)
    print("SEUIL CRITIQUE DE FRAIS")
    print("="*70)
    
    for config_name in configs.keys():
        config_data = results_df[results_df['config'] == config_name]
        
        # Trouver le seuil ou on passe sous le benchmark
        surperf_data = config_data[config_data['mean_return'] > benchmark_return]
        
        if len(surperf_data) > 0:
            max_fee = surperf_data['fee_pct'].max()
            print(f"\n{config_name}:")
            print(f"  Seuil max de frais pour surperformer: {max_fee*100:.2f}% par transaction")
            print(f"  Au-dela de ce seuil, la strategie sous-performe le benchmark")
        else:
            print(f"\n{config_name}:")
            print(f"  [ATTENTION] Ne surperforme meme pas avec 0% de frais!")
    
    print("\n" + "="*70)
    print("ANALYSE TERMINEE")
    print("="*70)
    
    return results_df


if __name__ == "__main__":
    results = main()
