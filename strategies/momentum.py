"""
Strategie de Momentum (suivi de tendance)
Acheter les actions ayant eu les meilleures performances passees
"""
import numpy as np
import pandas as pd
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class MomentumConfig:
    """Configuration de la strategie Momentum"""
    n_stocks: int = 20  # Nombre d'actions dans le portefeuille
    lookback_months: int = 12  # Periode de lookback pour le momentum (12 mois recommande)
    rebalancing_freq: str = 'M'  # Frequence de rebalancement: 'M' = mensuel, 'Q' = trimestriel
    init_cash: float = 100_000  # Capital initial
    seed: int = None  # Graine pour la reproductibilite (pour tie-breaking)


class MomentumStrategy:
    """
    Strategie qui :
    1. Selectionne les N actions avec le meilleur momentum (rendement sur lookback)
    2. Rebalance le portefeuille a chaque periode (mensuel/trimestriel)
    3. Poids egaux entre les actions selectionnees
    """
    
    def __init__(self, config: MomentumConfig = None):
        self.config = config or MomentumConfig()
        if self.config.seed:
            np.random.seed(self.config.seed)
    
    def calculate_momentum(self, prices: pd.DataFrame, lookback_days: int) -> pd.Series:
        """
        Calcule le momentum (rendement sur la periode de lookback)
        pour chaque action
        """
        if len(prices) < lookback_days:
            return pd.Series(0, index=prices.columns)
        
        # Prix au debut et a la fin de la periode
        start_prices = prices.iloc[-lookback_days]
        end_prices = prices.iloc[-1]
        
        # Calculer le rendement
        momentum = (end_prices - start_prices) / start_prices
        
        # Remplacer les NaN par -inf pour les exclure
        momentum = momentum.fillna(-np.inf)
        
        return momentum
    
    def get_rebalance_dates(self, prices: pd.DataFrame) -> pd.DatetimeIndex:
        """
        Genere les dates de rebalancement selon la frequence choisie
        """
        if self.config.rebalancing_freq == 'M':
            # Mensuel (debut de mois)
            dates = pd.date_range(start=prices.index[0], 
                                 end=prices.index[-1], 
                                 freq='MS')
        elif self.config.rebalancing_freq == 'Q':
            # Trimestriel (debut de trimestre)
            dates = pd.date_range(start=prices.index[0], 
                                 end=prices.index[-1], 
                                 freq='QS')
        else:
            # Par defaut: mensuel
            dates = pd.date_range(start=prices.index[0], 
                                 end=prices.index[-1], 
                                 freq='MS')
        
        # Filtrer pour ne garder que les dates presentes dans les donnees
        rebalance_dates = prices.index[prices.index.isin(dates)]
        
        # S'assurer qu'il y a au moins 2 dates
        if len(rebalance_dates) < 2:
            # Fallback: utiliser des intervalles reguliers
            interval = 63 if self.config.rebalancing_freq == 'Q' else 21  # ~3 mois ou ~1 mois
            rebalance_dates = prices.index[::interval]
        
        return rebalance_dates
    
    def run_backtest_simple(self, prices: pd.DataFrame, verbose: bool = False) -> Dict:
        """
        Execute le backtest avec une implementation simplifiee
        """
        all_stocks = prices.columns.tolist()
        
        # Parametres
        lookback_days = self.config.lookback_months * 21  # ~21 jours ouvres par mois
        n_stocks = min(self.config.n_stocks, len(all_stocks))
        init_cash = self.config.init_cash
        
        # Generer les dates de rebalancement
        rebalance_dates = self.get_rebalance_dates(prices)
        
        if verbose:
            print(f"Periode: {prices.index[0].strftime('%Y-%m-%d')} a {prices.index[-1].strftime('%Y-%m-%d')}")
            print(f"Nombre de rebalancements: {len(rebalance_dates)}")
            print(f"Frequence: {self.config.rebalancing_freq} (M=mensuel, Q=trimestriel)")
            print(f"Lookback: {self.config.lookback_months} mois")
        
        # Initialisation
        cash = init_cash
        holdings = {stock: 0 for stock in all_stocks}
        current_portfolio = []
        portfolio_values = []
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
            
            # Calculer le momentum pour selection
            hist_prices = prices.loc[:date]
            
            if len(hist_prices) >= lookback_days:
                momentum = self.calculate_momentum(hist_prices, lookback_days)
                
                # Selectionner les N actions avec le meilleur momentum
                # Filtrer les valeurs infinies
                valid_momentum = momentum[momentum != -np.inf]
                
                if len(valid_momentum) >= n_stocks:
                    top_stocks = valid_momentum.nlargest(n_stocks).index.tolist()
                    
                    if verbose and i < 3:
                        print(f"\n{date.strftime('%Y-%m-%d')} - Top {n_stocks} momentum:")
                        for j, stock in enumerate(top_stocks[:5]):
                            print(f"  {j+1}. {stock}: {momentum[stock]*100:.1f}%")
                    
                    # Determiner les achats et ventes
                    stocks_to_buy = [s for s in top_stocks if s not in current_portfolio]
                    stocks_to_sell = [s for s in current_portfolio if s not in top_stocks]
                    
                    # Vendre les actions sorties du top
                    for stock in stocks_to_sell:
                        if holdings[stock] > 0 and stock in current_prices.index:
                            cash += holdings[stock] * current_prices[stock]
                            holdings[stock] = 0
                            n_transactions += 1
                    
                    # Acheter les nouvelles actions du top
                    if stocks_to_buy:
                        allocation_per_stock = cash / len(stocks_to_buy)
                        for stock in stocks_to_buy:
                            if stock in current_prices.index and current_prices[stock] > 0:
                                qty = int(allocation_per_stock / current_prices[stock])
                                if qty > 0:
                                    holdings[stock] = qty
                                    cash -= qty * current_prices[stock]
                                    n_transactions += 1
                    
                    # Reequilibrer les poids si necessaire (optional)
                    # Pour l'instant on garde les positions existantes
                    
                    current_portfolio = top_stocks
        
        # Calculer les metriques finales
        final_value = portfolio_values[-1]['value'] if portfolio_values else init_cash
        total_return = (final_value - init_cash) / init_cash * 100
        
        # Calculer le Sharpe ratio et max drawdown
        values_df = pd.DataFrame(portfolio_values).set_index('date')
        returns = values_df['value'].pct_change().dropna()
        
        if len(returns) > 1 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # Annualise
            
            # Max drawdown
            cummax = values_df['value'].cummax()
            drawdown = (values_df['value'] - cummax) / cummax
            max_drawdown = drawdown.min() * 100
            
            # Volatilite annualisee
            volatility = returns.std() * np.sqrt(252) * 100
        else:
            sharpe_ratio = 0
            max_drawdown = 0
            volatility = 0
        
        if verbose:
            print(f"\n{'='*60}")
            print("RESULTATS")
            print(f"{'='*60}")
            print(f"Rendement total: {total_return:.2f}%")
            print(f"Sharpe ratio: {sharpe_ratio:.2f}")
            print(f"Max drawdown: {max_drawdown:.2f}%")
            print(f"Volatilite: {volatility:.2f}%")
            print(f"Nombre de transactions: {n_transactions}")
            print(f"Valeur finale: ${final_value:,.2f}")
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'volatility': volatility,
            'final_value': final_value,
            'initial_value': init_cash,
            'n_transactions': n_transactions,
            'portfolio_values': portfolio_values
        }


def run_monte_carlo_simulation(prices: pd.DataFrame, 
                               n_simulations: int = 100,
                               config: MomentumConfig = None) -> pd.DataFrame:
    """
    Execute N simulations Monte Carlo de la strategie Momentum
    
    Note: Pour le momentum deterministe, les graines n'affectent pas la selection,
    mais on garde la structure pour la coherence avec les autres strategies.
    """
    results = []
    
    print(f"Lancement de {n_simulations} simulations Monte Carlo (Momentum)...")
    
    for i in range(n_simulations):
        if (i + 1) % 10 == 0:
            print(f"  Simulation {i + 1}/{n_simulations}")
        
        # Creer une config avec une graine differente (pour eventuel tie-breaking)
        sim_config = MomentumConfig(
            n_stocks=config.n_stocks if config else 20,
            lookback_months=config.lookback_months if config else 12,
            rebalancing_freq=config.rebalancing_freq if config else 'M',
            init_cash=config.init_cash if config else 100_000,
            seed=i
        )
        
        strategy = MomentumStrategy(sim_config)
        result = strategy.run_backtest_simple(prices, verbose=False)
        
        if result:
            results.append({
                'simulation': i + 1,
                'seed': i,
                'total_return': result['total_return'],
                'sharpe_ratio': result['sharpe_ratio'],
                'max_drawdown': result['max_drawdown'],
                'volatility': result['volatility'],
                'final_value': result['final_value'],
                'n_transactions': result['n_transactions']
            })
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Test rapide si execute directement
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data.download_data import get_sp500_tickers, download_stock_data
    
    print("Test rapide de la strategie Momentum")
    print("="*60)
    
    # Chargement des donnees
    tickers = get_sp500_tickers(100)
    prices = download_stock_data(tickers, start_date='2018-01-01')
    
    # Test
    config = MomentumConfig(n_stocks=20, lookback_months=12, rebalancing_freq='M')
    strategy = MomentumStrategy(config)
    result = strategy.run_backtest_simple(prices, verbose=True)
    
    print("\n✓ Test OK")
