# Resultats Detailles par Strategie

## 1. Random + Stop-Loss

### Concept
Selectionner 20 actions aleatoirement dans le S&P 500, les remplacer si elles perdent plus de 10% sur 6 mois.

### Resultats

| Metrique | US (S&P 500) | Europe (EURO STOXX) |
|----------|--------------|---------------------|
| **Rendement** | 123% | 353% |
| **Benchmark** | 191% | 442% |
| **Surperformance** | **-68%** | **-89%** |
| **Sharpe Ratio** | 8.5 | 5.1 |
| **Max Drawdown** | -8% | -6% |
| **Transactions** | ~65 | ~80 |

### Analyse
- **Avantage** : Drawdown tres controle (-8% vs -34% marche)
- **Avantage** : Excellent ratio de Sharpe (8.5)
- **Inconvenient** : Sous-performe largement l'indice
- **Inconvenient** : Ne capture pas les phases de croissance

**Verdict :** Strategie defensive (preservation du capital), pas de croissance.

---

## 2. Momentum (Configuration de Base)

### Concept
Selectionner les 20 actions avec les meilleures performances sur 12 mois, rebalancement mensuel.

### Resultats

| Metrique | US | Europe |
|----------|-----|--------|
| **Rendement** | 117% | 296% |
| **Benchmark** | 191% | 442% |
| **Surperformance** | **-74%** | **-146%** |
| **Sharpe Ratio** | 8.6 | 4.6 |
| **Transactions** | 226 | ~200 |

### Analyse
- Avec les parametres par defaut (12 mois, 20 actions), le momentum ne surperforme pas
- Bon ratio de Sharpe (gestion du risque)
- Trop de transactions = frais eleves
- Lookback trop long = rentre tard dans les tendances

---

## 3. Momentum Optimise (Grid Search)

### Methodologie
Test systematique de 24 configurations :
- N actions : 10, 20, 30
- Lookback : 3, 6, 9, 12 mois
- Rebalancement : Mensuel (M) ou Trimestriel (Q)

### Configuration Optimale Identifiee

```
N actions:       10
Lookback:        3 mois
Rebalancement:   Trimestriel (Q)
```

### Resultats US (2018-2024)

#### Sans frais
| Metrique | Valeur |
|----------|--------|
| **Rendement** | **376%** |
| **Benchmark** | 191% |
| **Surperformance** | **+185%** |
| **Sharpe Ratio** | 7.6 |
| **Max Drawdown** | -19% |

#### Avec frais de transaction

| Frais/Tx | Rendement | Surperformance | Frais Totaux |
|----------|-----------|----------------|--------------|
| 0% | 376% | +185% | $0 |
| 0.1% | 359% | +168% | $10,387 |
| 0.5% | 267% | **+76%** | $44,215 |
| 1.0% | 236% | **+46%** | $83,248 |

**Resultat cle** : Meme avec **1% de frais par transaction**, la strategie surperforme encore de +46% !

### Resultats Europe (2010-2024)

| Periode | Strategie | Benchmark | Surperformance |
|---------|-----------|-----------|----------------|
| Complete 2010-2024 | 244% | **442%** | **-198%** |
| Crise Euro 2010-2012 | 15% | 23% | -7% |
| Brexit 2015-2017 | 1% | **41%** | -40% |
| Bull 2017-2020 | 15% | **41%** | -26% |
| COVID Crise | -16% | -28% | **+12%** |
| Inflation/Guerre 2022-2024 | 40% | 33% | **+7%** |

**Verdict Europe** :
- Surperformance sur **2/8 periodes** (25%)
- Fonctionne uniquement en periode de crise
- Rate completement les phases de croissance

---

## Comparaison US vs Europe

| Critere | US | Europe |
|---------|-------|-----------|
| Surperformance Momentum Optimal | **+76%** | **-198%** |
| % Periodes gagnantes | 100% | 25% |
| Sharpe moyen | 6.5 | 7.2 |
| Protection en crise | Oui | Oui |
| Capture de la hausse | Excellente | Faible |

### Pourquoi ca marche aux US mais pas en Europe ?

| Facteur | US | Europe |
|---------|-----|--------|
| **Concentration sectorielle** | Tech dominante (FAANG) | Secteurs fragmentes |
| **Momentum sectoriel** | Tres fort | Plus faible |
| **Liquidite** | Tres elevee | Plus faible |
| **Culture marche** | Growth-oriented | Value-oriented |

---

## Synthese Visuelle

Voir les graphiques detailles dans la section [Graphiques](Graphiques).
