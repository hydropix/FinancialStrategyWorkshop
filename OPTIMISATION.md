# Rapport d'Optimisation des Hyperparametres

## Resume Executif

L'optimisation par **Grid Search** a ete realisee sur **80 configurations** differentes avec **20 simulations Monte Carlo** par configuration (**1600 simulations au total**).

### Configuration Optimale Identifiee

Selon le critere du **Ratio de Sharpe** (equilibre rendement/risque) :

| Parametre | Configuration de Base | Configuration Optimale | Impact |
|-----------|----------------------|------------------------|--------|
| **Nombre d'actions** | 20 | **30** | +50% de diversification |
| **Lookback (mois)** | 6 | **3** | Reaction 2x plus rapide |
| **Stop-loss** | -10% | **-5%** | Protection renforcee |

### Resultats Compares (30 simulations)

| Metrique | Base (20/6/-10%) | Optimale (30/3/-5%) | Amelioration |
|----------|------------------|---------------------|--------------|
| **Rendement Moyen** | 124.4% | **136.9%** | +10.1% |
| **Rendement Median** | 127.5% | **135.9%** | +6.6% |
| **Ratio de Sharpe** | 8.52 | **8.97** | +5.3% |
| **Max Drawdown** | -8.1% | **-6.2%** | -23% (mieux) |
| **Win Rate** | 100% | **100%** | Stable |

---

## Methodologie

### Grille de Parametres Testes

```python
param_grid = {
    'n_stocks': [10, 15, 20, 25, 30],           # Diversification
    'lookback_months': [3, 6, 9, 12],           # Periode d'evaluation
    'stop_loss_threshold': [-5%, -10%, -15%, -20%]  # Seuil de sortie
}
```

**Total : 5 × 4 × 4 = 80 configurations**

### Criteres d'Optimisation

1. **Ratio de Sharpe** : Rendement ajuste a la volatilite
2. **Rendement Total** : Performance brute
3. **Rendement Ajuste au Risque** : Rendement / |Drawdown|
4. **Score Equilibre** : Moyenne normalisee (Sharpe + Rendement)

---

## Resultats Detailles

### 1. Meilleure Configuration par Critere

#### A. Ratio de Sharpe (9.04) ⭐ RECOMMANDE
```
N=30 actions | Lookback=3 mois | Stop-loss=-5%
- Rendement : 138.6%
- Sharpe    : 9.04
- Drawdown  : -6.2%
```

#### B. Rendement Total (148.8%)
```
N=30 actions | Lookback=6 mois | Stop-loss=-15%
- Rendement : 148.8%
- Sharpe    : 8.14
- Drawdown  : -9.6%
```

#### C. Rendement Ajuste au Risque (22.7)
```
N=15 actions | Lookback=3 mois | Stop-loss=-5%
- Rendement : 142.7%
- Sharpe    : 9.01
- Drawdown  : -6.3%
```

### 2. Insights Cles

**Parametre le plus impactant : Lookback**
- Lookback **court (3 mois)** = Meilleures performances
- Lookback **long (9-12 mois)** = Performances degradees
- Explication : Reactions plus rapides aux changements de tendance

**Parametre secondaire : Stop-Loss**
- Seuil **serre (-5%)** = Meilleur Sharpe, drawdown controle
- Seuil **lache (-20%)** = Rendement potentiellement plus eleve mais risque accru

**Parametre tertiaire : Nombre d'Actions**
- **30 actions** legerement meilleur que 20 (diversification)
- **10 actions** trop concentre (volatilite elevee)

---

## Zones d'Optimalite

### Zone "Sweet Spot" (Recommande)
```
- N : 25-30 actions
- Lookback : 3 mois
- Stop-loss : -5% a -10%
```
**Performance attendue :** Sharpe ~9.0, Rendement ~135-140%, Drawdown ~-6%

### Zone "Rendement Max" (Aggressif)
```
- N : 30 actions
- Lookback : 6 mois
- Stop-loss : -15%
```
**Performance attendue :** Rendement ~148%, mais Drawdown ~-10%

### Zone a Eviter
```
- Lookback : 9-12 mois (peu importe les autres parametres)
```
**Performance :** Sharpe degrade (< 8.0), drawdowns eleves

---

## Visualisations Generees

1. **optimization_heatmaps.png** : Cartes de chaleur des metriques vs parametres
2. **optimization_3d.png** : Surfaces de reponse 3D
3. **optimization_top10.png** : Top 10 configurations par critere

---

## Recommandations

### Pour un Investisseur Prudent (Conservateur)
**Config :** N=30, Lookback=3 mois, Stop-loss=-5%
- Ratio de Sharpe optimal (9.04)
- Drawdown minimise (-6.2%)
- Rendement solide (138.6%)

### Pour un Investisseur Equilibre
**Config :** N=25, Lookback=3 mois, Stop-loss=-10%
- Bon compromis rendement/risque
- Sharpe ~8.6, Rendement ~125%

### Pour un Investisseur Dynamique (Aggressif)
**Config :** N=30, Lookback=6 mois, Stop-loss=-15%
- Rendement maximal (148.8%)
- Accepte drawdown plus eleve (-9.6%)

---

## Limites et Considerations

1. **Couts de transaction** : Non inclus dans l'analyse (rebalancement frequent avec lookback=3mois)
2. **Periode de test** : 2018-2024 (bull market dominant)
3. **Univers d'actions** : S&P 500 uniquement
4. **Surapprentissage** : Risque de overfitting sur la periode testee

---

## Prochaines Etapes

1. **Test sur periodes stress** : 2008-2009, COVID-19
2. **Incorporation des couts** : Estimation realiste du slippage
3. **Walk-forward analysis** : Validation hors echantillon
4. **Optimisation dynamique** : Parametres adaptatifs selon le regime de marché

---

## Fichiers Generes

- `data/grid_search_results.csv` : Resultats complets des 80 configurations
- `data/comparison_baseline_optimized.csv` : Comparaison detaillee
- `charts/optimization_heatmaps.png` : Cartes de chaleur
- `charts/optimization_3d.png` : Visualisations 3D
- `charts/optimization_top10.png` : Top 10 configurations
