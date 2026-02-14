#!/usr/bin/env python3
"""
Analyse de l'impact des frais de transaction sur la strategie Momentum optimale
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from data.download_data import get_sp500_tickers, download_stock_data
from strategies.momentum import MomentumStrategy, MomentumConfig


def run_backtest_with_costs(prices, config, transaction_cost_pct=0.0, verbose=False):
    """
    Execute le backtest avec prise en compte des frais de transaction
    """
    all_stocks = prices.columns.tolist()
    
    lookback_days = config.lookback_months * 21
    n_stocks = min(config.n_stocks, len(all_stocks))
    init_cash = config.init_cash
    
    # Generer les dates de rebalancement
    if config.rebalancing_freq == 'M':
        dates = pd.date_range(start=prices.index[0], end=prices.index[-1], freq='MS')
    else:
        dates = pd.date_range(start=prices.index[0], end=prices.index[-1], freq='QS')
    
    rebalance_dates = prices.index[prices.index.isin(dates)]
    if len(rebalance_dates) < 2:
        interval = 63 if config.rebalancing_freq == 'Q' else 21
        rebalance_dates = prices.index[::interval]
    
    cash = init_cash
    holdings = {stock: 0 for stock in all_stocks}
    current_portfolio = []
    portfolio_values = []
    total_fees_paid = 0
    n_transactions = 0
    
    for i, date in enumerate(rebalance_dates):
        if date not in prices.index:
            continue
        
        current_prices = prices.loc[date]
        
        # Calculer la valeur du portefeuille
        portfolio_value = cash
        for stock, qty in holdings.items():
            if qty > 0 and stock in current_prices.index and not pd.isna(current_prices[stock]):
                portfolio_value += qty * current_prices[stock]
        
        portfolio_values.append({'date': date, 'value': portfolio_value})
        
        hist_prices = prices.loc[:date]
        
        if len(hist_prices) >= lookback_days:
            # Calculer momentum
            start_prices = hist_prices.iloc[-lookback_days]
            end_prices = hist_prices.iloc[-1]
            momentum = ((end_prices - start_prices) / start_prices).fillna(-np.inf)
            valid_momentum = momentum[momentum != -np.inf]
            
            if len(valid_momentum) >= n_stocks:
                top_stocks = valid_momentum.nlargest(n_stocks).index.tolist()
                
                # Transactions
                stocks_to_buy = [s for s in top_stocks if s not in current_portfolio]
                stocks_to_sell = [s for s in current_portfolio if s not in top_stocks]
                
                # Vendre avec frais
                for stock in stocks_to_sell:
                    if holdings[stock] > 0 and stock in current_prices.index:
                        sale_value = holdings[stock] * current_prices[stock]
                        fees = sale_value * transaction_cost_pct
                        cash += sale_value - fees
                        total_fees_paid += fees
                        holdings[stock] = 0
                        n_transactions += 1
                
                # Acheter avec frais
                if stocks_to_buy:
                    allocation_per_stock = cash / len(stocks_to_buy)
                    for stock in stocks_to_buy:
                        if stock in current_prices.index and current_prices[stock] > 0:
                            gross_qty = int(allocation_per_stock / current_prices[stock])
                            if gross_qty > 0:
                                gross_cost = gross_qty * current_prices[stock]
                                fees = gross_cost * transaction_cost_pct
                                net_cost = gross_cost + fees
                                if net_cost <= cash:
                                    qty = gross_qty
                                    holdings[stock] = qty
                                    cash -= net_cost
                                    total_fees_paid += fees
                                    n_transactions += 1
                
                current_portfolio = top_stocks
    
    # Metriques finales
    final_value = portfolio_values[-1]['value'] if portfolio_values else init_cash
    total_return = (final_value - init_cash) / init_cash * 100
    
    values_df = pd.DataFrame(portfolio_values).set_index('date')
    returns = values_df['value'].pct_change().dropna()
    
    if len(returns) > 1 and returns.std() > 0:
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        cummax = values_df['value'].cummax()
        drawdown = (values_df['value'] - cummax) / cummax
        max_drawdown = drawdown.min() * 100
        volatility = returns.std() * np.sqrt(252) * 100
    else:
        sharpe_ratio = 0
        max_drawdown = 0
        volatility = 0
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'volatility': volatility,
        'final_value': final_value,
        'initial_value': init_cash,
        'n_transactions': n_transactions,
        'total_fees_paid': total_fees_paid,
        'portfolio_values': portfolio_values
    }


def run_monte_carlo_with_costs(prices, config, n_simulations=30, transaction_cost_pct=0.0):
    """Monte Carlo avec frais"""
    results = []
    
    for i in range(n_simulations):
        sim_config = MomentumConfig(
            n_stocks=config.n_stocks,
            lookback_months=config.lookback_months,
            rebalancing_freq=config.rebalancing_freq,
            init_cash=config.init_cash,
            seed=i
        )
        
        result = run_backtest_with_costs(prices, sim_config, transaction_cost_pct, verbose=False)
        
        if result:
            results.append({
                'total_return': result['total_return'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'volatility': result['volatility'],
                'n_transactions': result['n_transactions'],
                'total_fees_paid': result['total_fees_paid'],
                'final_value': result['final_value']
            })
    
    return pd.DataFrame(results)


def main():
    print("="*70)
    print("ANALYSE DES FRAIS - MOMENTUM OPTIMAL")
    print("="*70)
    print("\nConfiguration optimale identifiee:")
    print("  - N actions: 10")
    print("  - Lookback: 3 mois")
    print("  - Rebalancement: Trimestriel")
    
    # Chargement
    print("\n[1] Chargement des donnees...")
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2010-01-01', end_date='2024-12-31')
    
    # Config optimale
    config = MomentumConfig(
        n_stocks=10,
        lookback_months=3,
        rebalancing_freq='Q',
        init_cash=100_000
    )
    
    # Benchmark
    bench_returns = prices.pct_change().mean(axis=1).dropna()
    bench_cumulative = (1 + bench_returns).cumprod()
    benchmark_return = (bench_cumulative.iloc[-1] - 1) * 100
    
    print(f"  Benchmark (Buy & Hold): {benchmark_return:.1f}%")
    
    # ============================================================
    # TEST AVEC DIFFERENTS NIVEAUX DE FRAIS
    # ============================================================
    print("\n[2] Test avec differents niveaux de frais...")
    print("="*70)
    
    fee_levels = [
        (0.0, "0%"),
        (0.001, "0.1%"),
        (0.002, "0.2%"),
        (0.005, "0.5%"),
        (0.01, "1.0%")
    ]
    
    results_summary = []
    
    for fee_pct, fee_label in fee_levels:
        print(f"\n[Frais: {fee_label} par transaction]")
        
        mc_results = run_monte_carlo_with_costs(
            prices=prices,
            config=config,
            n_simulations=30,
            transaction_cost_pct=fee_pct
        )
        
        mean_return = mc_results['total_return'].mean()
        mean_sharpe = mc_results['sharpe_ratio'].mean()
        mean_dd = mc_results['max_drawdown'].mean()
        mean_txn = mc_results['n_transactions'].mean()
        mean_fees = mc_results['total_fees_paid'].mean()
        outperf = mean_return - benchmark_return
        
        results_summary.append({
            'fee_pct': fee_pct,
            'fee_label': fee_label,
            'return': mean_return,
            'sharpe': mean_sharpe,
            'drawdown': mean_dd,
            'transactions': mean_txn,
            'total_fees': mean_fees,
            'outperformance': outperf
        })
        
        print(f"  Rendement:     {mean_return:7.1f}%")
        print(f"  Sharpe:        {mean_sharpe:7.2f}")
        print(f"  Drawdown:      {mean_dd:7.1f}%")
        print(f"  Transactions:  {mean_txn:7.0f}")
        print(f"  Frais totaux:  ${mean_fees:,.0f}")
        print(f"  Surperf:       {outperf:+7.1f}%")
    
    # ============================================================
    # TABLEAU RECAPITULATIF
    # ============================================================
    print("\n[3] TABLEAU RECAPITULATIF")
    print("="*70)
    print(f"{'Frais':<8} {'Return':<10} {'Sharpe':<8} {'DD':<8} {'Txns':<8} {'Frais $':<12} {'Surperf':<10}")
    print("-"*70)
    
    for r in results_summary:
        print(f"{r['fee_label']:<8} {r['return']:>8.1f}%  {r['sharpe']:>6.2f}  "
              f"{r['drawdown']:>6.1f}%  {r['transactions']:>6.0f}  "
              f"${r['total_fees']:>8,.0f}  {r['outperformance']:>+7.1f}%")
    
    # ============================================================
    # ANALYSE
    # ============================================================
    print("\n[4] ANALYSE DE ROBUSTESSE AUX FRAIS")
    print("="*70)
    
    # Trouver le seuil de rentabilite
    positive_outperf = [r for r in results_summary if r['outperformance'] > 0]
    
    if positive_outperf:
        max_fees = max(r['fee_pct'] for r in positive_outperf)
        print(f"\nSurperformance positive jusqu'a: {max_fees*100:.1f}% de frais par transaction")
        
        # Impact par 0.1%
        r0 = results_summary[0]
        r1 = results_summary[1]
        impact_per_01pct = (r0['return'] - r1['return']) / 1  # 0.1% = 1 niveau
        print(f"Impact par 0.1% de frais: -{impact_per_01pct:.1f} points de rendement")
    else:
        print("\nSurperformance negative meme sans frais")
    
    # Comparaison avec config de base (20, 12, M)
    print("\n[5] COMPARAISON AVEC CONFIGURATION DE BASE")
    print("="*70)
    print("\nConfiguration de base (20 actions, 12 mois, Mensuel):")
    
    base_config = MomentumConfig(n_stocks=20, lookback_months=12, rebalancing_freq='M')
    base_results = run_monte_carlo_with_costs(prices, base_config, n_simulations=30, transaction_cost_pct=0.005)
    
    base_return = base_results['total_return'].mean()
    base_sharpe = base_results['sharpe_ratio'].mean()
    base_txn = base_results['n_transactions'].mean()
    base_outperf = base_return - benchmark_return
    
    print(f"  Avec 0.5% de frais:")
    print(f"    Return: {base_return:.1f}% | Sharpe: {base_sharpe:.2f} | Txns: {base_txn:.0f} | Surperf: {base_outperf:+.1f}%")
    
    opt_results = [r for r in results_summary if r['fee_pct'] == 0.005][0]
    print(f"\nConfiguration optimale (10 actions, 3 mois, Trimestriel):")
    print(f"  Avec 0.5% de frais:")
    print(f"    Return: {opt_results['return']:.1f}% | Sharpe: {opt_results['sharpe']:.2f} | "
          f"Txns: {opt_results['transactions']:.0f} | Surperf: {opt_results['outperformance']:+.1f}%")
    
    print(f"\nAvantage de la config optimale: {opt_results['return'] - base_return:+.1f}% de rendement")
    
    # Sauvegarde
    df_summary = pd.DataFrame(results_summary)
    df_summary.to_csv('data/momentum_costs_analysis.csv', index=False)
    print("\n[OK] Resultats sauvegardes dans: data/momentum_costs_analysis.csv")
    
    return results_summary


if __name__ == "__main__":
    results = main()
