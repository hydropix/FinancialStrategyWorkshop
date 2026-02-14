# Graphiques et Visualisations

Tous les graphiques sont disponibles dans le dossier `charts/` du repo principal.

---

## Vue d'Ensemble

### Comparaison des Strategies

![Comparaison des strategies](https://raw.githubusercontent.com/hydropix/FinancialStrategyWorkshop/main/charts/wiki_summary_charts.png)

**Ce graphique montre :**
- **US** : Le Momentum Optimal (376%) bat largement le S&P 500 (191%)
- **Europe** : Aucune strategie active ne bat l'indice EURO STOXX (442%)
- **Impact des frais** : Meme avec 1% de frais, le Momentum reste avantageux aux US

---

## Analyse Temporelle

### Performance par Periode Historique

![Analyse par periode](https://raw.githubusercontent.com/hydropix/FinancialStrategyWorkshop/main/charts/wiki_period_analysis.png)

**Observations cles :**

**Etats-Unis (2018-2024)**
- Surperformance sur **toutes les periodes** (5/5)
- Protection efficace en bear market 2022 (0% vs -9%)
- Capture partielle de la hausse en bull market

**Europe (2010-2024)**
- Sous-performance chronique sauf en crise
- Protection en COVID (perd moins que l'indice)
- Rate completement les phases de croissance

---

## Optimisation

### Grid Search Momentum

![Heatmap Grid Search](https://raw.githubusercontent.com/hydropix/FinancialStrategyWorkshop/main/charts/wiki_gridsearch_heatmap.png)

**Heatmap des 24 configurations testees**

**Configuration optimale** (case verte foncee) :
- **10 actions**, **3 mois lookback**, **trimestriel**
- Rendement : **376%**

**Patterns observes :**
1. **Plus le lookback est court, mieux c'est** (3 mois > 12 mois)
2. **10 actions > 20 ou 30** (concentration maximale)
3. **Trimestriel > Mensuel** (moins de frais, moins de bruit)

---

## Conclusions

### Synthese Visuelle Finale

![Conclusions](https://raw.githubusercontent.com/hydropix/FinancialStrategyWorkshop/main/charts/wiki_conclusion.png)

**Ce graphique resume les 5 lecons cles :**

1. **Taux de reussite** : 100% aux US, 25% en Europe
2. **Erosion par les frais** : Impact significatif mais strategie reste viable
3. **Complexite vs Performance** : La strategie la plus complexe gagne aux US, mais la plus simple suffit
4. **Recommandation** : ETF pour 99% des investisseurs

---

## Autres Graphiques Disponibles

Les graphiques suivants sont aussi dans le repo :

- `monte_carlo_analysis.png` - Distribution des resultats Monte Carlo
- `transaction_costs_impact.png` - Impact detaille des frais
- `optimization_heatmaps.png` - Heatmaps d'optimisation completes
- `multi_market_comparison.png` - Comparaison US vs Europe

---

## Generer les Graphiques

Pour regenerer tous les graphiques :

```bash
python generate_wiki_charts.py
```

Les fichiers seront crees dans `charts/wiki_*.png`.
