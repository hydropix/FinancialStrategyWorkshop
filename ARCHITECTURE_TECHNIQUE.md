# Documentation Technique Complète

## Guide de Réutilisation de l'Architecture

Ce document décrit en détail tous les composants techniques pour réutiliser ce cadre dans un nouveau projet.

---

## 1. Fichiers Source Essentiels

### 1.1 Classe de Base Stratégie

**Fichier:** `strategies/random_stoploss.py` (utiliser comme template)

```python
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import numpy as np

@dataclass
class StrategyConfig:
    """Configuration standardisée"""
    n_stocks: int = 20
    init_cash: float = 100_000
    seed: int = None
    # Ajoutez vos paramètres spécifiques

class BaseStrategy:
    """Classe de base à hériter"""
    
    def __init__(self, config: StrategyConfig):
        self.config = config
        if config.seed:
            np.random.seed(config.seed)
    
    def run_backtest_simple(self, prices: pd.DataFrame, verbose: bool = False) -> Dict:
        """
        Méthode principale à implémenter
        
        Args:
            prices: DataFrame avec dates en index, tickers en colonnes
            verbose: Afficher les détails
            
        Returns:
            Dict avec au minimum:
            - total_return: float (pourcentage)
            - sharpe_ratio: float
            - max_drawdown: float (pourcentage négatif)
            - final_value: float
        """
        raise NotImplementedError()
```

### 1.2 Téléchargement de Données

**Fichier:** `data/download_data.py`

```python
# Fonction principale à réutiliser
def download_stock_data(tickers: List[str], 
                       start_date: str = '2018-01-01',
                       end_date: str = '2024-12-31',
                       cache_dir: str = 'data') -> pd.DataFrame:
    """
    Télécharge les prix avec cache automatique
    Retourne DataFrame: index=dates, colonnes=tickers
    """
```

**Usage:**
```python
from data.download_data import download_stock_data

tickers = ['AAPL', 'MSFT', 'GOOGL']  # Votre univers
prices = download_stock_data(tickers, start_date='2010-01-01')
# prices est un DataFrame prêt à l'emploi
```

### 1.3 Monte Carlo

**Fichier:** `strategies/random_stoploss.py` (fonction `run_monte_carlo_simulation`)

```python
def run_monte_carlo_simulation(prices: pd.DataFrame, 
                               n_simulations: int = 100,
                               config: StrategyConfig = None) -> pd.DataFrame:
    """
    Exécute N simulations avec graines différentes
    
    Args:
        prices: DataFrame des prix
        n_simulations: Nombre de runs (recommandé: 50-100)
        config: Configuration de la stratégie
        
    Returns:
        DataFrame avec colonnes:
        - simulation: numéro de run
        - total_return: rendement total
        - sharpe_ratio: ratio de Sharpe
        - max_drawdown: drawdown max
    """
```

---

## 2. Pipeline de Test Complet

### Script Type pour Nouvelle Stratégie

**Fichier:** Créer `test_ma_strategie.py`

```python
#!/usr/bin/env python3
"""
Template pour tester une nouvelle stratégie
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 1. IMPORTS
from data.download_data import get_sp500_tickers, download_stock_data
from strategies.ma_strategie import MaStrategie, MaConfig  # Votre stratégie

# 2. CONFIGURATION
def main():
    print("="*70)
    print("TEST NOUVELLE STRATEGIE")
    print("="*70)
    
    # 2.1 Chargement données
    print("\n[1/5] Chargement des données...")
    tickers = get_sp500_tickers(100)  # Ou votre propre liste
    prices = download_stock_data(tickers, start_date='2010-01-01')
    
    # 2.2 Configuration
    print("\n[2/5] Configuration...")
    config = MaConfig(
        n_stocks=20,
        # Vos paramètres
        seed=42
    )
    
    # 2.3 Test individuel
    print("\n[3/5] Test individuel...")
    strategy = MaStrategie(config)
    result = strategy.run_backtest_simple(prices, verbose=True)
    
    print(f"\n  Résultats:")
    print(f"    - Rendement: {result['total_return']:.2f}%")
    print(f"    - Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"    - Drawdown: {result['max_drawdown']:.2f}%")
    
    # 2.4 Monte Carlo
    print("\n[4/5] Monte Carlo (50 simulations)...")
    from strategies.ma_strategie import run_monte_carlo_simulation
    mc_results = run_monte_carlo_simulation(prices, n_simulations=50, config=config)
    
    # 2.5 Analyse
    print("\n[5/5] Analyse statistique...")
    print(f"  Rendement moyen: {mc_results['total_return'].mean():.2f}%")
    print(f"  Sharpe moyen: {mc_results['sharpe_ratio'].mean():.2f}")
    print(f"  Std rendement: {mc_results['total_return'].std():.2f}%")
    
    # Benchmark
    benchmark = prices.pct_change().mean(axis=1).cumsum().iloc[-1] * 100
    print(f"\n  vs Benchmark: {mc_results['total_return'].mean() - benchmark:+.2f}%")
    
    # Sauvegarder
    mc_results.to_csv('data/ma_strategie_results.csv', index=False)
    print("\n✓ Résultats sauvegardés dans data/ma_strategie_results.csv")
    
    return mc_results

if __name__ == "__main__":
    results = main()
```

---

## 3. Analyse des Frais (CRITIQUE)

### Fichier: `analyze_transaction_costs.py`

**Réutilisation directe:**

```python
from analyze_transaction_costs import TransactionCostAnalyzer, run_monte_carlo_with_costs

# Tester avec différents niveaux de frais
fee_levels = [0.0, 0.001, 0.005, 0.01]  # 0%, 0.1%, 0.5%, 1%

for fee in fee_levels:
    results = run_monte_carlo_with_costs(
        prices=prices,
        config=config,
        n_simulations=30,
        transaction_cost_pct=fee
    )
    print(f"Frais {fee*100:.1f}%: Rendement = {results['total_return'].mean():.1f}%")
```

---

## 4. Techniques de Visualisation

### Graphiques Standards

```python
import matplotlib.pyplot as plt

def plot_equity_curves(results_df, save_path='charts/equity_curves.png'):
    """Courbes de capital"""
    fig, ax = plt.subplots(figsize=(12, 6))
    # Votre code ici
    plt.savefig(save_path)

def plot_distribution(results_df, metric='total_return', save_path='charts/distribution.png'):
    """Distribution d'une métrique"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(results_df[metric], bins=20, alpha=0.7)
    ax.axvline(results_df[metric].mean(), color='red', linestyle='--', label='Moyenne')
    plt.savefig(save_path)
```

---

## 5. Tests Multi-Marchés

### Utiliser `test_multiple_markets_periods.py`

Modifier pour ajouter votre stratégie:

```python
# Dans compare_markets()

# Votre stratégie
from strategies.ma_strategie import MaStrategie, MaConfig

config = MaConfig(...)

# Test US
us_results = test_market(us_prices, "US S&P 500", config, periods_dict)

# Test Europe
eu_results = test_market(eu_prices, "Europe", config, periods_dict)

# Combiner
all_results = pd.concat([us_results, eu_results])
```

---

## 6. Gestion des Dépendances

### Fichier: `requirements.txt`

```txt
# OBLIGATOIRE
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.0

# Backtesting
vectorbt>=0.28.0

# Visualisation
matplotlib>=3.7.0
plotly>=5.14.0

# Analyse
scipy>=1.10.0
scikit-learn>=1.3.0

# Notebook (optionnel)
jupyter>=1.0.0
```

---

## 7. Commandes Utiles

### Installation Rapide

```bash
# 1. Cloner
git clone https://github.com/hydropix/FinancialStrategyWorkshop.git
cd FinancialStrategyWorkshop

# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 3. Installation
pip install -r requirements.txt

# 4. Test
python run_strategy.py
```

### Workflow Quotidien

```bash
# Nouvelle stratégie
cp strategies/random_stoploss.py strategies/momentum.py

# Éditer momentum.py
# ...

# Test rapide
python -c "
from strategies.momentum import MomentumStrategy, MomentumConfig
from data.download_data import download_stock_data
import pandas as pd

prices = download_stock_data(['AAPL', 'MSFT'], '2020-01-01', '2024-12-31')
config = MomentumConfig(n_stocks=2)
strategy = MomentumStrategy(config)
result = strategy.run_backtest_simple(prices)
print(f'Rendement: {result[\"total_return\"]:.1f}%')
"

# Test complet
python test_momentum.py

# Analyse frais
python analyze_transaction_costs.py --strategy momentum

# Commit
git add strategies/momentum.py test_momentum.py
git commit -m "Ajout strategie Momentum"
```

---

## 8. Checklist Anti-Erreurs

### Avant de Lancer un Test Long

- [ ] Vérifier que `prices` n'a pas de NaN: `prices.isna().sum().sum() == 0`
- [ ] Vérifier les dates: `prices.index[0]`, `prices.index[-1]`
- [ ] Vérifier n_actions > config.n_stocks
- [ ] Vérifier que les rendements ne sont pas tous identiques (bug)
- [ ] Faire un test sur 10 jours d'abord (rapide)

### Debug Rapide

```python
# Vérifier les données
print(prices.head())
print(prices.tail())
print(f"Shape: {prices.shape}")
print(f"NaN: {prices.isna().sum().sum()}")

# Vérifier le résultat
result = strategy.run_backtest_simple(prices)
print(result)  # Doit contenir toutes les clés requises
```

---

## 9. Extensions Possibles

### Ajouter des Données Fondamentales

```python
import yfinance as yf

def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'pe_ratio': info.get('trailingPE'),
        'pb_ratio': info.get('priceToBook'),
        'dividend_yield': info.get('dividendYield'),
        'market_cap': info.get('marketCap')
    }
```

### Optimisation Bayésienne (au lieu de Grid Search)

```bash
pip install scikit-optimize
```

```python
from skopt import gp_minimize

# Définir la fonction objectif
def objective(params):
    config = StrategyConfig(n_stocks=int(params[0]), ...)
    result = run_single_test(config)
    return -result['sharpe_ratio']  # Négatif car on minimise

# Optimiser
result = gp_minimize(objective, dimensions, n_calls=50)
```

---

## 10. Références et Documentation

### Fichiers de Référence dans ce Projet

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `strategies/random_stoploss.py` | 200 | Template complet |
| `run_strategy.py` | 150 | Script principal type |
| `analyze_transaction_costs.py` | 400 | Analyse frais complète |
| `test_multiple_markets_periods.py` | 350 | Test multi-marchés |
| `optimize_strategy.py` | 450 | Grid search avancé |

### Documentation Externe

- **VectorBT:** https://vectorbt.dev/
- **YFinance:** https://github.com/ranaroussi/yfinance
- **Pandas:** https://pandas.pydata.org/docs/

---

## 11. Template de Nouveau Projet

```bash
# Créer nouveau projet basé sur cette architecture
mkdir MonProjetStrategies
cd MonProjetStrategies

# Copier la structure
mkdir -p strategies data analysis visualization tests config

# Copier les fichiers essentiels
cp ../FinancialStrategyWorkshop/data/download_data.py data/
cp ../FinancialStrategyWorkshop/strategies/random_stoploss.py strategies/base_template.py

# Créer requirements.txt
cat > requirements.txt << EOF
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.0
matplotlib>=3.7.0
vectorbt>=0.28.0
EOF

# Installer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Premier test
python -c "
from data.download_data import download_stock_data
prices = download_stock_data(['AAPL'], '2023-01-01', '2024-12-31')
print('✓ Setup OK')
"
```

---

## Résumé des Points Clés

1. **Toujours tester avec frais** (0.1% - 0.5% minimum)
2. **Toujours faire du Monte Carlo** (50+ simulations)
3. **Toujours tester multi-marchés** si possible
4. **Documenter les paramètres** utilisés
5. **Versionner** avec Git à chaque étape

Ce cadre est maintenant prêt à être réutilisé pour n'importe quelle stratégie quantitative !
