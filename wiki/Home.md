# Financial Strategy Workshop

> **TL;DR** : Apres avoir teste 25+ configurations sur 2 marches et 15+ periodes historiques, le **Buy & Hold d'indice** reste la meilleure strategie pour 90% des investisseurs.

---

## Vue d'Ensemble

Ce workshop a pour objectif de tester empiriquement differentes strategies d'investissement systematiques et de comparer leurs performances avec un simple **Buy & Hold d'indice**.

### Strategies Testees

1. **Random Selection + Stop-Loss** : Selection aleatoire avec regle d'eviction
2. **Momentum** : Achat des actions aux meilleures performances passees
3. **Momentum Optimise** : Grid search des hyperparametres optimaux

### Marches Analyses

- **Etats-Unis** (S&P 500) : 2018-2024
- **Europe** (EURO STOXX) : 2010-2024

---

## Resultats en 30 secondes

| Strategie | US (S&P 500) | Europe | Verdict |
|-----------|--------------|--------|---------|
| Buy & Hold Indice | +191% | +442% | Gagnant |
| Random + Stop-Loss | +123% | +353% | Sous-performe |
| Momentum (Base) | +117% | +296% | Sous-performe |
| **Momentum Optimal** | **+376%** | +244% | US uniquement |

**Configuration optimale identifiee :**
- 10 actions
- Lookback 3 mois
- Rebalancement trimestriel
- Marche US uniquement

---

## Navigation

- [Resultats Detailles](Resultats-Detailles) - Analyse complete par strategie
- [Graphiques](Graphiques) - Visualisations des performances
- [Methodologie](Methodologie) - Comment reproduire les tests
- [Conclusions](Conclusions) - Lecons apprises et recommandations
- [References](References) - Papers et ressources

---

## Conclusion Principale

> **Pour 99% des investisseurs, un simple ETF World ou S&P 500 en Buy & Hold reste la meilleure strategie.**

Les strategies actives testees :
- Ne surperforment que sur certains marches (US growth)
- Echouent sur l'Europe
- Generent beaucoup de frais de transaction
- Requierent une discipline difficile a maintenir

---

**Date :** 2026-02-14  
**Auteur :** @hydropix  
**Repo :** https://github.com/hydropix/FinancialStrategyWorkshop
