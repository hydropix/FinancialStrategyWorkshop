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
├── strategies/
│   └── random_stoploss.py          # Implementation de la strategie
├── data/
│   ├── download_data.py
│   ├── stock_prices.csv
│   ├── monte_carlo_results.csv
│   ├── optimized_monte_carlo_results.csv
│   └── transaction_costs_analysis.csv  # Analyse des frais
├── charts/
│   ├── monte_carlo_analysis.png
│   ├── optimization_heatmaps.png
│   └── transaction_costs_impact.png    # Impact des frais
├── run_strategy.py                   # Strategie de base
├── run_optimized_strategy.py         # Strategie optimisee
├── optimize_strategy.py              # Grid search
├── analyze_transaction_costs.py      # Analyse des frais
├── RESULTATS.md                      # Resultats initiaux
├── OPTIMISATION.md                   # Rapport d'optimisation
├── FRAIS_ET_SURPERFORMANCE.md        # ⭐ Analyse frais/surperformance
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

## ⚠️ RESULTATS CLES - A LIRE EN PRIORITE

**❌ La strategie NE SURPERFORME PAS l'indice**, meme sans frais de transaction.

| | Configuration Base | Configuration Optimale | Benchmark S&P 500 |
|---|-------------------|------------------------|-------------------|
| **Rendement** | 123% | 130% | **191%** |
| **Surperformance** | **-68pp** | **-61pp** | - |
| **Sharpe Ratio** | 8.5 | 8.9 | 0.9 |
| **Max Drawdown** | -8% | -6% | -34% |

**👉 Conclusion :** C'est une strategie **DEFENSIVE** (preservation du capital), pas de **CROISSANCE**.

Voir [FRAIS_ET_SURPERFORMANCE.md](FRAIS_ET_SURPERFORMANCE.md) pour l'analyse complete des frais et surperformance.

### Configuration Optimale (avec frais 0.5%)

| Parametre | Valeur | Impact |
|-----------|--------|--------|
| N actions | 30 | Diversification max |
| Lookback | 6 mois (pas 3) | Moins de transactions = moins de frais |
| Stop-loss | -10% | Equilibre rendement/risk |

### Impact des Frais de Transaction

La strategie genere **beaucoup de transactions** :
- Config Base : ~65 transactions sur 7 ans
- Config Optimisee (3 mois) : ~174 transactions sur 7 ans

**Cout avec 1% de frais par transaction :**
- Perte de performance : -8 a -13 points de pourcentage
- Cout total sur $100k : $4,000 - $8,600

**Recommandation :** Si vous utilisez cette strategie, preferez la **configuration Base** (20 actions, 6 mois, -10%) qui genere moins de frais.

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
