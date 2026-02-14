"""
Strategie de selection aleatoire avec regle d'eviction (stop-loss sur 6 mois)
"""
import numpy as np
import pandas as pd
import vectorbt as vbt
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class StrategyConfig:
    """Configuration de la strategie"""
    n_stocks: int = 20  # Nombre d'actions dans le portefeuille
    lookback_months: int = 6  # Periode de lookback pour le stop-loss
    stop_loss_threshold: float = -0.10  # Seuil de stop-loss (-10%)
    init_cash: float = 100_000  # Capital initial
    seed: int = None  # Graine pour la reproductibilite


class RandomStopLossStrategy:
    """
    Strategie qui :
    1. Selectionne N actions aleatoirement
    2. Verifie chaque mois la performance sur 6 mois
    3. Si performance < -10%, evince l'action et en prend une nouvelle au hasard
    """
    
    def __init__(self, config: StrategyConfig = None):
        self.config = config or StrategyConfig()
        if self.config.seed:
            np.random.seed(self.config.seed)
    
    def calculate_performance(self, prices: pd.DataFrame, lookback_days: int) -> pd.Series:
        """Calcule la performance sur la periode de lookback"""
        recent_prices = prices.iloc[-lookback_days:]
        if len(recent_prices) < 2:
            return pd.Series(0, index=prices.columns)
        
        perf = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]
        return perf
    
    def run_backtest_simple(self, prices: pd.DataFrame, verbose: bool = False) -> Dict:
        """
        Execute le backtest avec une implementation simplifiee
        """
        all_stocks = prices.columns.tolist()
        
        # Parametres
        lookback_days = self.config.lookback_months * 21  # ~21 jours ouvres par mois
        n_stocks = self.config.n_stocks
        init_cash = self.config.init_cash
        
        # Generer les dates de rebalancement (debut de mois)
        rebalance_dates = pd.date_range(start=prices.index[0], 
                                       end=prices.index[-1], 
                                       freq='MS')
        rebalance_dates = prices.index[prices.index.isin(rebalance_dates)]
        
        if len(rebalance_dates) < 2:
            # Utiliser tous les mois disponibles
            rebalance_dates = prices.index[::21]  # Tous les 21 jours environ
        
        # Initialisation du portefeuille
        current_portfolio = np.random.choice(all_stocks, size=n_stocks, replace=False).tolist()
        cash = init_cash
        holdings = {stock: 0 for stock in all_stocks}
        portfolio_values = []
        
        if verbose:
            print(f"Portefeuille initial: {current_portfolio}")
        
        for i, date in enumerate(rebalance_dates):
            if date not in prices.index:
                continue
                
            current_prices = prices.loc[date]
            
            # Calculer la valeur du portefeuille
            portfolio_value = cash
            for stock, qty in holdings.items():
                if qty > 0 and stock in current_prices.index:
                    portfolio_value += qty * current_prices[stock]
            
            portfolio_values.append({'date': date, 'value': portfolio_value})
            
            if i == 0:
                # Premier rebalancement - achat initial
                allocation_per_stock = init_cash / n_stocks
                for stock in current_portfolio:
                    if stock in current_prices.index and current_prices[stock] > 0:
                        qty = int(allocation_per_stock / current_prices[stock])
                        holdings[stock] = qty
                        cash -= qty * current_prices[stock]
            else:
                # Verifier les actions a evincer
                hist_prices = prices.loc[:date]
                
                if len(hist_prices) >= lookback_days:
                    performances = self.calculate_performance(hist_prices, lookback_days)
                    
                    stocks_to_evict = []
                    for stock in current_portfolio:
                        if stock in performances.index:
                            if performances[stock] < self.config.stop_loss_threshold:
                                stocks_to_evict.append(stock)
                    
                    if len(stocks_to_evict) > 0:
                        if verbose:
                            print(f"{date.strftime('%Y-%m-%d')} - Actions evincees: {stocks_to_evict}")
                        
                        # Vendre les actions evincees
                        for stock in stocks_to_evict:
                            if holdings[stock] > 0 and stock in current_prices.index:
                                cash += holdings[stock] * current_prices[stock]
                                holdings[stock] = 0
                        
                        # Selectionner de nouvelles actions
                        available = [s for s in all_stocks if s not in current_portfolio]
                        n_to_add = len(stocks_to_evict)
                        
                        if len(available) >= n_to_add:
                            new_stocks = np.random.choice(available, size=n_to_add, replace=False).tolist()
                            
                            # Mettre a jour le portefeuille
                            for old_stock in stocks_to_evict:
                                current_portfolio.remove(old_stock)
                            current_portfolio.extend(new_stocks)
                            
                            # Acheter les nouvelles actions
                            allocation_per_stock = cash / n_to_add if n_to_add > 0 else 0
                            for stock in new_stocks:
                                if stock in current_prices.index and current_prices[stock] > 0:
                                    qty = int(allocation_per_stock / current_prices[stock])
                                    holdings[stock] = qty
                                    cash -= qty * current_prices[stock]
        
        # Calculer les metriques finales
        final_value = portfolio_values[-1]['value'] if portfolio_values else init_cash
        total_return = (final_value - init_cash) / init_cash * 100
        
        # Calculer le Sharpe ratio approximatif
        values_df = pd.DataFrame(portfolio_values).set_index('date')
        returns = values_df['value'].pct_change().dropna()
        
        if len(returns) > 1 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # Annualise
            
            # Max drawdown
            cummax = values_df['value'].cummax()
            drawdown = (values_df['value'] - cummax) / cummax
            max_drawdown = drawdown.min() * 100
        else:
            sharpe_ratio = 0
            max_drawdown = 0
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': final_value,
            'portfolio_values': portfolio_values,
            'initial_value': init_cash
        }


def run_monte_carlo_simulation(prices: pd.DataFrame, 
                               n_simulations: int = 100,
                               config: StrategyConfig = None) -> pd.DataFrame:
    """
    Execute N simulations Monte Carlo de la strategie avec differentes graines
    """
    results = []
    
    print(f"Lancement de {n_simulations} simulations Monte Carlo...")
    
    for i in range(n_simulations):
        if (i + 1) % 10 == 0:
            print(f"  Simulation {i + 1}/{n_simulations}")
        
        # Creer une config avec une graine differente
        sim_config = StrategyConfig(
            n_stocks=config.n_stocks if config else 20,
            lookback_months=config.lookback_months if config else 6,
            stop_loss_threshold=config.stop_loss_threshold if config else -0.10,
            seed=i
        )
        
        strategy = RandomStopLossStrategy(sim_config)
        result = strategy.run_backtest_simple(prices, verbose=False)
        
        if result:
            results.append({
                'simulation': i + 1,
                'seed': i,
                'total_return': result['total_return'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'final_value': result['final_value']
            })
    
    return pd.DataFrame(results)
