# Financial Strategy Workshop

Outil d'analyse et de backtesting de strategies d'investissement en bourse.

## Description

Ce projet permet de tester, comparer et analyser differentes strategies d'investissement sur des donnees historiques d'actions. Il utilise des simulations Monte Carlo pour evaluer la robustesse des strategies.

## Strategie Implementee

### Random Selection + Stop-Loss

**Concept :**
- Selection aleatoire de N actions dans un univers defini
- Rebalancement periodique avec regle d'eviction
- Si performance sur M mois < -X%, l'action est remplacee

**Parametres testes :**
- N = 20 actions
- M = 6 mois de lookback
- X = -10% de seuil de stop-loss
- Univers = S&P 500 (top 100 capitalisations)
- Periode = 2018-2024

## Structure du Projet

```
FinancialStrategyWorkshop/
├── strategies/              # Implementation des strategies
│   └── random_stoploss.py  # Strategie random + stop-loss
├── backtesting/            # Moteur de backtest
├── analysis/               # Outils d'analyse
├── data/                   # Donnees historiques
│   ├── download_data.py   # Telechargement YFinance
│   ├── stock_prices.csv   # Donnees brutes
│   ├── monte_carlo_results.csv
│   └── summary_statistics.csv
├── notebooks/              # Notebooks Jupyter
├── dashboard/              # Interface Dash (futur)
├── charts/                 # Graphiques generes
├── run_strategy.py         # Script principal
├── visualize_results.py    # Visualisation
├── requirements.txt        # Dependances
└── README.md
```

## Installation

```bash
# Creer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer les dependances
pip install vectorbt yfinance pandas numpy matplotlib plotly
```

## Utilisation

### 1. Lancer le backtest principal

```bash
python run_strategy.py
```

Ce script va :
1. Telecharger les donnees du S&P 500 (top 100)
2. Executer une simulation individuelle avec affichage des details
3. Lancer 50 simulations Monte Carlo
4. Generer les statistiques de performance
5. Sauvegarder les resultats dans `data/`

### 2. Generer les visualisations

```bash
python visualize_results.py
```

Genere des graphiques dans le dossier `charts/` :
- Distribution des rendements
- Distribution des ratios de Sharpe
- Distribution des drawdowns
- Scatter plot rendement vs risque

## Resultats Cles

Voir [RESULTATS.md](RESULTATS.md) pour l'analyse complete.

**Resume :**
- Rendement moyen : 127.31% (vs 190.86% pour le S&P 500)
- Ratio de Sharpe moyen : 8.43 (excellent)
- Max Drawdown moyen : -8.18% (tres controle)
- 100% des simulations positives
- 0% des simulations battent le benchmark

## Technologies Utilisees

- **Python 3.12+**
- **vectorbt** : Backtesting et analyse de portefeuille
- **yfinance** : Telechargement des donnees Yahoo Finance
- **pandas/numpy** : Manipulation de donnees
- **matplotlib/plotly** : Visualisation

## Personnalisation

Pour tester d'autres parametres, modifier le fichier `run_strategy.py` :

```python
config = StrategyConfig(
    n_stocks=20,                    # Nombre d'actions
    lookback_months=6,              # Periode de lookback
    stop_loss_threshold=-0.10,      # Seuil de stop-loss (-10%)
    init_cash=100_000,              # Capital initial
    seed=42                         # Graine aleatoire
)
```

## Limitations et Ameliorations Futures

**Limitations actuelles :**
- Pas de prise en compte des couts de transaction
- Pas de gestion des dividendes
- Rebalancement simplifie (pas d'optimisation fiscale)

**Ameliorations prevues :**
- [ ] Ajouter des couts de transaction realistes
- [ ] Implementer d'autres strategies (momentum, value, etc.)
- [ ] Creer une interface Dash interactive
- [ ] Optimisation des parametres (grid search)
- [ ] Tests sur differentes periodes historiques

## Licence

Ce projet est open-source a des fins educatives.

## Avertissement

**Ce logiciel est a but educatif uniquement. Ne pas risquer de l'argent que vous ne pouvez pas vous permettre de perdre.**
