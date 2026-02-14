# Methodologie

Comment reproduire les tests et verifier les resultats.

---

## Architecture du Projet

```
FinancialStrategyWorkshop/
|
├── strategies/              # Implementations des strategies
│   ├── random_stoploss.py   # Random + Stop-Loss
│   └── momentum.py          # Momentum (base + optimal)
|
├── data/                    # Donnees et cache
│   ├── download_data.py     # Telechargement YFinance
│   ├── stock_prices.csv     # Donnees US (S&P 500)
│   └── european_prices_clean.csv  # Donnees EU
|
├── charts/                  # Graphiques generes
│   ├── wiki_summary_charts.png
│   ├── wiki_period_analysis.png
│   ├── wiki_gridsearch_heatmap.png
│   └── wiki_conclusion.png
|
├── run_strategy.py          # Test Random + Stop-Loss
├── test_momentum.py         # Test Momentum base
├── optimize_momentum.py     # Grid Search
├── test_momentum_multimarket.py    # Tests multi-marches
├── analyze_momentum_costs.py       # Analyse des frais
└── generate_wiki_charts.py  # Generation des graphiques
```

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/hydropix/FinancialStrategyWorkshop.git
cd FinancialStrategyWorkshop
```

### 2. Creer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dependances

```bash
pip install pandas numpy yfinance vectorbt matplotlib
```

---

## Lancer les Tests

### Test 1 : Random + Stop-Loss

```bash
python run_strategy.py
```

**Sortie attendue :**
- Simulation individuelle avec details
- Monte Carlo (50 simulations)
- Statistiques de performance
- Comparaison avec benchmark

### Test 2 : Momentum (Configuration Base)

```bash
python test_momentum.py
```

**Parametres testes :**
- 20 actions
- 12 mois lookback
- Rebalancement mensuel

### Test 3 : Grid Search (Optimisation)

```bash
python optimize_momentum.py
```

**Teste 24 configurations :**
- N actions : 10, 20, 30
- Lookback : 3, 6, 9, 12 mois
- Frequence : Mensuel, Trimestriel

**Duree :** ~5-10 minutes

### Test 4 : Multi-Marches

```bash
python test_momentum_multimarket.py
```

**Teste sur :**
- US : 2018-2024 (sous-periodes COVID, Bear, Bull)
- Europe : 2010-2024 (sous-periodes crises)

### Test 5 : Analyse des Frais

```bash
python analyze_momentum_costs.py
```

**Teste avec frais :**
- 0%, 0.1%, 0.2%, 0.5%, 1.0%

### Test 6 : Generation des Graphiques

```bash
python generate_wiki_charts.py
```

**Genere 4 graphiques :**
- Comparaison des strategies
- Analyse par periode
- Heatmap Grid Search
- Conclusions

---

## Methodologie des Tests

### 1. Monte Carlo Simulation

Pour chaque configuration :
- 30 simulations avec graines differentes
- Reduction du biais de selection
- Mesure de la robustesse

### 2. Benchmark

**Buy & Hold equi-poids :**
- Moyenne de toutes les actions disponibles
- Poids egaux (pas de capitalisation)
- Rebalancement quotidien implicite

### 3. Metriques Calculees

| Metrique | Formule | Interpretation |
|----------|---------|----------------|
| Total Return | (Vf - Vi) / Vi | Rendement brut |
| Sharpe Ratio | (Rp - Rf) / sigma_p | Rendement ajuste au risque |
| Max Drawdown | min(V - Vmax) / Vmax | Perte maximale |
| Volatilite | sigma * sqrt(252) | Risque annualise |

### 4. Gestion des Frais

**Modele de couts :**
```python
# Achat
frais = montant * taux_frais
cout_total = montant + frais

# Vente
frais = montant * taux_frais
produit_net = montant - frais
```

---

## Technologies Utilisees

| Outil | Usage | Version |
|-------|-------|---------|
| Python | Langage principal | 3.12+ |
| pandas | Manipulation de donnees | 2.0+ |
| numpy | Calculs numeriques | 1.24+ |
| yfinance | Telechargement donnees | 0.2+ |
| vectorbt | Backtesting (optionnel) | 0.28+ |
| matplotlib | Visualisation | 3.7+ |

---

## Reproductibilite

### Graines Aleatoires

Toutes les simulations utilisent des graines fixes pour la reproductibilite :
```python
seed = 42  # ou i pour Monte Carlo
np.random.seed(seed)
```

### Cache des Donnees

Les donnees Yahoo Finance sont telechargees une fois et stockees :
- `data/stock_prices.csv` (US)
- `data/european_prices_clean.csv` (EU)

Pour forcer le retelechargement : supprimer les fichiers CSV.

---

## Limites Connues

1. **Survivorship Bias** : Les donnees ne contiennent que les entreprises existantes
2. **Frais reels** : Modele simplifie (pas de slippage, pas de taxes)
3. **Liquidite** : Hypothese de liquidite parfaite
4. **Periodes** : Tests sur 7-14 ans, pas de garantie sur 30+ ans

---

## Validation

Pour verifier que tout fonctionne :

```bash
# Test rapide
python -c "from strategies.momentum import MomentumStrategy; print('OK')"

# Test donnees
python -c "from data.download_data import download_stock_data; print('OK')"

# Test complet (1 simulation)
python test_momentum.py
```

---

## Contribuer

Pour tester une nouvelle strategie :

1. Creer `strategies/ma_strategie.py`
2. Implementer `run_backtest_simple()`
3. Creer `test_ma_strategie.py`
4. Lancer et comparer

Voir `strategies/random_stoploss.py` comme template.
