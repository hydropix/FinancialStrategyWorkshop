# Test Multi-Marchés et Multi-Périodes

## Résumé

Test de la stratégie Random + Stop-Loss sur :
- **Marché Européen** (53 actions, 2010-2024)
- **Périodes de crise** : Crise de la dette 2010-2012, COVID-19, Crise énergétique 2022

## Résultats sur le Marché Européen

| Période | Strategie | Benchmark | Surperformance | Win Rate |
|---------|-----------|-----------|----------------|----------|
| **EU 2010-2024** | 352.9% | 441.5% | **-88.6pp** | 10% |
| **Crise Dette 2010-2012** | 16.4% | 22.5% | **-6.2pp** | 20% |
| **COVID Crash 2020** | -21.9% | -20.5% | **-1.3pp** | 27% |
| **Crise Energie 2022** | -3.7% | -2.7% | **-1.0pp** | 30% |

### Analyse par Période

#### 1. Période Complète (2010-2024)
- Gap important vs benchmark : -88.6 points de pourcentage
- Win rate très faible : 10% seulement des simulations battent l'indice
- Le marché européen a fortement monté sur cette période (+441%)

#### 2. Crise de la Dette Européenne (2010-2012)
- Surperformance négative : -6.2pp
- Période de stagnation du marché européen (+22.5%)
- La stratégie n'a pas protégé efficacement

#### 3. COVID-19 Crash (Fév-Mai 2020)
- Performance similaire au marché (-21.9% vs -20.5%)
- Très légère sous-performance
- Le stop-loss n'a pas empêché les pertes en crash rapide

#### 4. Crise Énergétique 2022
- Performance proche du marché (-3.7% vs -2.7%)
- Meilleure période relative (seulement -1.0pp)

## Comparaison US vs Europe

| Marché | Période | Surperf Stratégie | Remarque |
|--------|---------|-------------------|----------|
| US S&P 500 | 2018-2024 | **-67pp** | Bull market |
| Europe | 2010-2024 | **-89pp** | Inclus crises |

**Constat :** La sous-performance est encore plus marquée en Europe qu'aux US.

## Conclusions

### 1. La Stratégie ne Surperforme sur AUCUNE Période

Sur l'ensemble des périodes testées :
- **0%** de surperformance
- **100%** de sous-performance
- Même pendant les crises, la stratégie ne bat pas le marché

### 2. Efficacité du Stop-Loss Remise en Question

Le stop-loss à -10% n'a pas permis de :
- Protéger en période de crash (COVID)
- Surperformer en période de crise prolongée (Dette 2010-2012)
- Créer de la valeur ajoutée vs un simple buy & hold

### 3. Marché Européen vs Américain

La sous-performance est **plus marquée en Europe** (-89pp vs -67pp) :
- Marché européen plus fragmenté
- Moins de "big tech" porteuses
- Stratégie random pénalisée par la dispersion sectorielle

## Recommandations Actualisées

### ❌ Ne PAS Utiliser Cette Stratégie Pour :
- Surperformer le marché européen
- Protéger en période de crise
- Remplacer un ETF indiciel

### ✅ Utiliser SEULEMENT Pour :
- Apprentissage / Pédagogie
- Composante très défensive (max 10-15% de l'allocation)
- Stratégie "satellite" dans un portefeuille diversifié

### Paramètres si Utilisé en Europe

Avec les frais européens (souvent plus élevés) :
```python
n_stocks=20
lookback_months=6  # Minimum pour limiter les frais
stop_loss_threshold=-0.15  # Moins serré qu'aux US
```

**Attention** : Les frais de transaction sont souvent plus élevés en Europe (Tobin tax sur certains marchés).

## Limites de l'Analyse

1. **Période US limitée** : Données S&P 500 uniquement depuis 2018
2. **Survivorship bias** : Actions européennes actuelles uniquement
3. **Frais réels** : Non inclus (peuvent être élevés en Europe)
4. **Impôt** : Non pris en compte

## Fichiers Générés

- `data/european_prices_clean.csv` : Données européennes (53 actions)
- `data/multi_market_results.csv` : Résultats des tests
- `charts/multi_market_comparison.png` : Visualisations comparatives
- `charts/multi_market_table.png` : Tableau récapitulatif
