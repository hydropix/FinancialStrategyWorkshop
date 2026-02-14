# Plan d'Investigation Stratégies d'Investissement

## Objectif
Trouver une stratégie systématique qui surperforme le Buy & Hold d'indice (ETF) sur le long terme, après frais de transaction.

---

## Architecture du Projet (Réutilisable)

### Structure des Dossiers

```
FinancialStrategyWorkshop/
├── strategies/              # Implémentations des stratégies
│   ├── base.py             # Classe de base abstraite
│   ├── random_stoploss.py  # Exemple: Random + Stop-Loss
│   └── [votre_strategie].py # Nouvelles stratégies
├── backtesting/            # Moteur de backtest
│   └── engine.py          # Wrapper pour simulations
├── data/                   # Données et cache
│   ├── download_data.py   # Téléchargement YFinance
│   ├── stock_prices.csv   # Cache données US
│   └── european_prices_clean.csv  # Cache données EU
├── analysis/               # Analyse de résultats
│   ├── monte_carlo.py     # Simulations Monte Carlo
│   └── metrics.py         # Calculs de métriques
├── visualization/          # Graphiques
│   └── plots.py          # Fonctions de visualisation
├── tests/                  # Scripts de test
│   ├── test_strategy.py   # Test single stratégie
│   └── compare_strategies.py  # Comparaison multi-stratégies
├── config/                 # Configurations
│   └── parameters.yaml    # Paramètres des stratégies
├── notebooks/              # Exploration Jupyter
├── charts/                 # Sorties graphiques
├── data/                   # Résultats CSV
└── docs/                   # Documentation
    ├── ARCHITECTURE.md     # Ce fichier
    └── RESULTATS.md        # Résultats des tests
```

---

## Fichiers Clés à Réutiliser

### 1. Infrastructure de Base

| Fichier | Description | Réutilisation |
|---------|-------------|---------------|
| `data/download_data.py` | Téléchargement YFinance | ✅ Directe |
| `data/download_european_data_v2.py` | Données EU | ✅ Directe |
| `strategies/random_stoploss.py` | Exemple d'implémentation | ✅ Référence |

### 2. Moteur de Backtest

```python
# Copier cette structure pour chaque nouvelle stratégie
class NouvelleStrategie:
    def __init__(self, config):
        self.config = config
    
    def run_backtest_simple(self, prices, verbose=False):
        # Logique de la stratégie
        # Retourner: dict avec 'total_return', 'sharpe_ratio', 'max_drawdown'
        pass

def run_monte_carlo_simulation(prices, n_simulations, config):
    # Utiliser cette fonction existante
    # ou créer une version adaptée
    pass
```

### 3. Analyse des Frais

| Fichier | Fonction | Usage |
|---------|----------|-------|
| `analyze_transaction_costs.py` | `TransactionCostAnalyzer` | **OBLIGATOIRE** - Tester avec frais réalistes |

---

## Liste des Stratégies à Tester

### Niveau 1: Stratégies Classiques (Commencer ici)

#### 1.1 Momentum (Tendance)
```python
# Concept: Acheter ce qui monte, vendre ce qui baisse
# Implémentation:
- Calculer le rendement sur 12 mois
- Sélectionner les top 20% performers
- Rebalancement mensuel/trimestriel
```
**Fichier:** `strategies/momentum.py`

#### 1.2 Mean Reversion (Retour à la Moyenne)
```python
# Concept: Acheter ce qui a baissé, vendre ce qui a monté
# Implémentation:
- Calculer le Z-score sur 20 jours
- Acheter si Z-score < -2 (survendu)
- Vendre si Z-score > +2 (suracheté)
```
**Fichier:** `strategies/mean_reversion.py`

#### 1.3 Dual Momentum (Gary Antonacci)
```python
# Concept: Momentum absolu + relatif
# Implémentation:
- Comparer rendement 12 mois vs Treasury bills (momentum absolu)
- Sélectionner les top secteurs/pays (momentum relatif)
- Sortir en cash si momentum négatif
```
**Fichier:** `strategies/dual_momentum.py`

### Niveau 2: Stratégies Factorielles

#### 2.1 Value (Ben Graham Style)
```python
# Concept: Acheter bon marché, vendre cher
# Métriques:
- P/E ratio faible
- P/B ratio faible
- Dividend yield élevé
- FCF yield élevé
```
**Données nécessaires:** Données fondamentales (YFinance peut fournir certaines)

#### 2.2 Quality (Actions de Qualité)
```python
# Concept: Robesse financière
# Métriques:
- ROE élevé et stable
- Faible ratio dette/capitaux propres
- Earnings stability
```

#### 2.3 Low Volatility
```python
# Concept: Moins volatile = meilleur rendement risk-adjusted
# Implémentation:
- Sélectionner les 20% actions moins volatiles (beta < 1)
- Backtest: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1340483
```

### Niveau 3: Stratégies Avancées

#### 3.1 Trend Following (Suivi de Tendance)
```python
# Concept: Suivre la tendance du marché global
# Signaux:
- SMA 200 jours: Investi si prix > SMA200
- Sortir si prix < SMA200
- Backtest sur S&P 500 complet
```

#### 3.2 Seasonality (Saisonnalité)
```python
# Concept: "Sell in May and go away"
- Investi Nov-Avril
- Cash Mai-Octobre
- Ou variations sectorielles
```

#### 3.3 Volatility Targeting
```python
# Concept: Ajuster l'exposition selon la volatilité
- Volatilité faible → 100% actions
- Volatilité élevée → Réduire l'exposition
- Objectif: Volatilité constante (ex: 10%)
```

### Niveau 4: Stratégies Combinées

#### 4.1 Multi-Factor
```python
# Combiner Value + Momentum + Quality
- Scorer chaque action sur chaque facteur
- Sélectionner les meilleures au total
- Exemple: QVAL, QMOM ETFs
```

#### 4.2 Risk Parity
```python
# Allouer selon l'inverse de la volatilité
- Pas égal poids, mais égal risque
- Actions volatiles = petites positions
- Actions stables = grandes positions
```

#### 4.3 Adaptive Asset Allocation
```python
# Mélanger plusieurs classes d'actifs
- Actions, Obligations, Or, Cash
- Sélectionner dynamiquement les meilleures
- Momentum cross-asset
```

---

## Processus de Test Standardisé

### Étape 1: Implémentation (30 min)

```python
# 1. Créer le fichier strategies/[nom].py
# 2. Implémenter la logique
# 3. Tester sur une seule période

# Template:
class MaStrategie:
    def __init__(self, config):
        self.config = config
        
    def run_backtest(self, prices):
        # Votre logique ici
        return {
            'total_return': ...,  # %
            'sharpe_ratio': ...,  # ratio
            'max_drawdown': ...,  # %
            'final_value': ...     # $
        }
```

### Étape 2: Monte Carlo (1h)

```bash
python run_strategy.py --strategy MaStrategie --n-simulations 100
```

### Étape 3: Analyse des Frais (1h)

```bash
python analyze_transaction_costs.py --strategy MaStrategie
```

**ATTENTION:** Beaucoup de stratégies "marchent" sans frais mais échouent avec 0.5%+ de frais.

### Étape 4: Multi-Marchés (2h)

```bash
python test_multiple_markets.py --strategy MaStrategie
```

- Tester sur US 2007-2024 (si données disponibles)
- Tester sur Europe 2010-2024
- Tester sur périodes de crise

### Étape 5: Walk-Forward (3h)

```python
# Validation hors échantillon
# Entraîner sur 2007-2015, tester sur 2016-2020
# Entraîner sur 2010-2018, tester sur 2019-2024
```

---

## Checklist de Validation

Avant de considérer une stratégie comme "viable":

- [ ] **Surperformance positive** vs benchmark (même de 1-2%)
- [ ] **Sharpe ratio > 1.0** (après frais)
- [ ] **Max drawdown < 25%** (mieux que marché)
- [ ] **Win rate > 50%** en Monte Carlo
- [ ] **Robustesse** sur plusieurs périodes (pas juste 2010-2020)
- [ ] **Frais supportables** : Impact < 2% de performance
- [ ] **Multi-marchés** : Fonctionne sur US ET Europe
- [ ] **Walk-forward** : Performances similaires in/out sample

---

## Techniques Utilisées (Récapitulatif)

### Techniques Statistiques
1. **Monte Carlo Simulation** : Tester la robustesse avec 50-100 graines aléatoires
2. **Grid Search** : Optimisation des hyperparamètres
3. **Walk-Forward Analysis** : Validation hors échantillon temporelle
4. **Bootstrapping** : Rééchantillonnage des rendements

### Métriques de Performance
1. **Total Return** : Rendement total brut
2. **Sharpe Ratio** : Rendement ajusté au risque
3. **Sortino Ratio** : Sharpe modifié (pénalise que downside)
4. **Max Drawdown** : Perte maximale depuis pic
5. **Calmar Ratio** : Rendement / Max DD
6. **Win Rate** : % de trades gagnants (ou périodes)

### Gestion des Données
1. **Cache local** : Éviter de retélécharger
2. **Forward Fill** : Gestion des valeurs manquantes
3. **Survivorship bias check** : Vérifier que les données ne contiennent pas que des gagnants
4. **Outliers handling** : Gestion des splits/dividendes

---

## Prochaines Étapes Recommandées

### Priorité 1: Momentum (1-2 jours)
**Pourquoi ?** La plus documentée, simple à implémenter, fonctionne souvent.

```bash
# Créer
strategies/momentum.py
test_momentum.py

# Paramètres à tester
lookback_periods = [3, 6, 9, 12]  # mois
n_top_stocks = [10, 20, 30]
rebalancing = ['M', 'Q']  # Mensuel, Trimestriel
```

### Priorité 2: Dual Momentum (2-3 jours)
**Pourquoi ?** Protège en bear market, très populaire.

### Priorité 3: Trend Following (1-2 jours)
**Pourquoi ?** Extrêmement simple, peu de transactions = faibles frais.

---

## Ressources

### Livres
- "Quantitative Momentum" - Wes Gray
- "Dual Momentum Investing" - Gary Antonacci
- "What Works on Wall Street" - James O'Shaughnessy

### Papers
- Fama-French 3-Factor Model
- Carhart 4-Factor Model (ajoute Momentum)
- Asness Value-Momentum

### ETFs à Étudier
- MTUM (iShares Momentum)
- VLUE (iShares Value)
- QUAL (iShares Quality)
- QVAL (Alpha Architect Value)

---

## Commandes Git pour Nouveau Projet

```bash
# 1. Cloner le template
git clone https://github.com/hydropix/FinancialStrategyWorkshop.git NouveauProjet
cd NouveauProjet

# 2. Créer nouvelle branche
git checkout -b strategie-momentum

# 3. Implémenter la stratégie
# ... coder ...

# 4. Commit et push
git add .
git commit -m "Ajout strategie Momentum"
git push origin strategie-momentum
```

---

## Questions à se Poser Pour Chaque Stratégie

1. **Pourquoi ça marcherait ?** (Story/Logique économique)
2. **Sur quelle période historique ça marche ?**
3. **Sur quelle période ça échoue ?** (Drawdowns)
4. **Combien de transactions ?** (Frais)
5. **Est-ce reproductible ?** (Monte Carlo)
6. **Pourquoi ça continuerait à marcher ?** (Pas de overfitting)

---

## Contact / Support

Projet GitHub: https://github.com/hydropix/FinancialStrategyWorkshop

Pour toute question sur l'utilisation de cette architecture, référez-vous aux fichiers:
- `README.md` : Utilisation de base
- `ARCHITECTURE.md` : Structure technique complète
- `RESULTATS.md` : Exemple de rapport de résultats
