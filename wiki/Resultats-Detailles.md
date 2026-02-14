# Resultats de l'Analyse - Strategie Random + Stop-Loss

## Resume de la Strategie

**Description :**
- Selection aleatoire de 20 actions parmi le S&P 500 (top 100 capitalisations)
- Rebalancement mensuel
- Regle d'eviction : Si performance sur 6 mois < -10%, l'action est remplacee par une nouvelle selection aleatoire
- Capital initial : $100,000
- Periode d'analyse : 2018-01-02 a 2024-12-30 (7 ans)

## Resultats des Simulations Monte Carlo (n=50)

### Metriques Principales

| Metrique | Moyenne | Mediane | Ecart-type | Min | Max | P5 | P95 |
|----------|---------|---------|------------|-----|-----|----|-----|
| **Rendement Total** | 127.31% | 132.19% | 22.90% | 83.58% | 170.01% | 87.83% | 160.27% |
| **Ratio de Sharpe** | 8.43 | 8.43 | 1.03 | 6.19 | 11.33 | 7.07 | 10.16 |
| **Max Drawdown** | -8.18% | -7.97% | 2.99% | -19.02% | -3.61% | -13.18% | -4.49% |

### Distribution des Resultats

**Rendement Total :**
- 100% des simulations sont positives
- 0% des simulations battent le benchmark (S&P 500 equipondere : 190.86%)
- 100% des simulations > 50%
- 0% des simulations < -20%

**Ratio de Sharpe :**
- Excellent ratio de Sharpe moyen de 8.43
- Toutes les simulations ont un Sharpe > 6

**Drawdown :**
- Drawdown moyen controle a -8.18%
- Maximum de -19.02% (valeur aberrante)
- 75% des simulations ont un drawdown < -9.11%

## Comparaison avec le Benchmark

| | Strategie Random + SL | Benchmark S&P 500 | Difference |
|---|----------------------|-------------------|------------|
| Rendement Total | 127.31% | 190.86% | -63.55% |
| Max Drawdown | -8.18% | ~-34% (est.) | +25.82% |
| Ratio de Sharpe | 8.43 | ~0.9 (est.) | +7.53 |

### Analyse

**Points Positifs :**
1. **Risque tres bien controle** : Drawdown moyen de seulement -8.18% vs ~-34% pour le S&P 500
2. **Ratio de Sharpe excellent** : 8.43 vs ~0.9 pour le S&P 500
3. **Toutes les simulations sont positives** : 100% de succes
4. **Rebalancement actif efficace** : La regle de stop-loss permet de limiter les pertes

**Points Negatifs :**
1. **Sous-performance en rendement** : -63.55% par rapport au benchmark
2. **Aucune simulation ne bat le benchmark** : La strategie est trop conservative
3. **Cout de transaction** : Non pris en compte dans cette analyse

## Interpretation

La strategie de selection aleatoire avec stop-loss de -10% sur 6 mois produit :
- Un **portefeuille tres defensif** avec peu de volatilite
- Un **rendement positif mais moderne** (127% sur 7 ans = ~12.8% annualise)
- Une **excellente gestion du risque** avec des drawdowns minimaux

Le stop-loss agit comme un filtre qui elimine les actions en difficulte, mais il elimine aussi les actions qui pourraient rebondir. Sur la periode 2018-2024 (bull market apres COVID), cette approche conservative a rate une partie de la hausse.

## Conclusion

Cette strategie serait adaptee pour :
- Des investisseurs **risk-averse** cherchant a preserver leur capital
- Un **contexte de marché bearish** ou incertain
- Une **composante defensive** d'un portefeuille plus large

Elle n'est pas adaptee pour :
- Maximiser le rendement sur le long terme
- Un investisseur cherchant a battre le marché
- Une periode de bull market prolongee

## Fichiers Generes

- `data/stock_prices.csv` : Donnees historiques telechargees
- `data/monte_carlo_results.csv` : Resultats detailles des 50 simulations
- `data/summary_statistics.csv` : Statistiques recapitulatives
- `charts/monte_carlo_analysis.png` : Visualisations des distributions
- `charts/monte_carlo_boxplots.png` : Boxplots des metriques

## Prochaines Etapes Suggerées

1. Tester avec differents seuils de stop-loss (-5%, -15%, -20%)
2. Tester avec differents horizons de lookback (3 mois, 12 mois)
3. Ajouter des couts de transaction realistes
4. Comparer avec d'autres strategies (momentum, value, etc.)
5. Tester sur differentes periodes (crise 2008, COVID, etc.)
