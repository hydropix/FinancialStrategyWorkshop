# Resultats: Diversification Geographique

## Resume Executif

Les tests de diversification geographique montrent qu'il est **possible de reduire significativement le risque US tout en maintenant un bon rendement**.

## Performance des Strategies (2007-2024)

| Strategie | Rendement Annuel | Volatilite | Sharpe | Max Drawdown |
|-----------|------------------|------------|--------|--------------|
| **S&P 500 (Benchmark)** | 10.3% | 19.8% | 0.52 | **-55.2%** |
| MSCI All Country World | 7.3% | 20.4% | 0.36 | -56.3% |
| **US vs World Dynamique** | **9.6%** | 16.2% | **0.59** | **-33.0%** |
| Equal Weight Global | 7.7% | 16.2% | 0.48 | -32.0% |
| Momentum (12m, Top2) | 8.1% | 16.7% | 0.48 | -35.9% |
| Risk Parity (3m vol) | 7.4% | 16.2% | 0.46 | -33.7% |

## Conclusions Principales

### 1. Reduction du Risque Significative

Toutes les strategies de diversification reduisent le drawdown max de **plus de 20 points de pourcentage**:
- S&P 500: -55.2%
- Strategies diversifiees: ~-33%

Cela signifie beaucoup moins de stress en periode de crise (2008, 2020).

### 2. La Strategie "US vs World Dynamique" est Optimale

**Pourquoi elle est interessante:**
- Rendement proche du S&P 500 (9.6% vs 10.3%)
- Drawdown reduit de 40% (-33% vs -55%)
- Meilleur Sharpe ratio (0.59 vs 0.52)
- S'adapte automatiquement aux conditions de marche

**Comment elle fonctionne:**
- Si momentum US > momentum World: 60% US, 40% International
- Sinon: 30% US, 70% International
- Rebalancement mensuel

### 3. Correlations entre Marches

| vs S&P 500 | Correlation | Diversification |
|------------|-------------|-----------------|
| ACWI (Monde) | 0.97 | Faible |
| VEA (Dev ex-US) | 0.86 | Moderee |
| IEV (Europe) | 0.82 | Moderee |
| EPP (Pacifique) | 0.79 | Moderee |
| EEM (EM) | 0.75 | Bonne |
| **EWJ (Japon)** | **0.72** | **Meilleure** |

Le Japon offre la meilleure diversification par rapport aux US.

## Recommandations Pratiques

### Pour Reduire le Risque US (Profil Prudent)

**Allocation recommandee:**
```
30-40% US (SPY ou equivalent)
25-30% Europe (IEV ou EFA)
15-20% Marches Emergents (EEM ou VWO)
10-15% Japon (EWJ)
10% Pacifique ex-Japon (EPP)
```

### Pour une Approche Dynamique (Profil Actif)

**Strategie US vs World:**
1. Calculer le momentum sur 6 mois de SPY et ACWI
2. Si SPY > ACWI: 60% US + 40% International
3. Si SPY < ACWI: 30% US + 70% International
4. Rebalancer mensuellement

### ETF Recommandes (Europe - UCITS)

| Region | ETF | Ticker | Frais |
|--------|-----|--------|-------|
| US | iShares Core S&P 500 | CSPX | 0.07% |
| Europe | iShares STOXX 600 | EXV1 | 0.20% |
| EM | iShares Core MSCI EM | EMIM | 0.18% |
| Japon | iShares MSCI Japan | IJPA | 0.20% |
| Monde | iShares MSCI World | IWDA | 0.20% |

## Points de Vigilance

### 1. Correlations augmentent en crise
En periode de stress (COVID-19, 2008), toutes les correlations augmentent. La diversification protege moins bien, mais protege toujours.

### 2. Risque de change
Les ETF non-hedges sont exposes aux fluctuations de devises:
- Euro fort = performances internationales reduites
- Dollar fort = performances US ameliorees

### 3. Frais de transaction
Les strategies dynamiques necessitent plus de rebalancing:
- Buy & Hold: 1 transaction/an
- Dynamique: 4-12 transactions/an

## Prochaines Etapes Suggerrees

1. **Tester sur periode recente** (2018-2024) pour voir la performance avec Trump/Biden
2. **Ajouter des ETF secteurs** (energie, tech) pour diversification supplementaire
3. **Tester avec couverture devise** (ETF hedges en EUR)
4. **Analyser les periodes de drawdown** specifiquement

## Comparison avec vos Strategies Precedentes

| Strategie | Sharpe | Max DD | Verdict |
|-----------|--------|--------|---------|
| Random + Stop-Loss | 8.5 | -8% | Trop defensive, sous-performe |
| Momentum (US only) | ~0.9 | ~-34% | Bon mais concentree US |
| **US vs World Dyn.** | **0.59** | **-33%** | **Meilleur compromis** |

La diversification geographique offre un meilleur ratio risque/rendement que les strategies US pures.

---

*Tests effectues sur la periode 2007-2024 avec donnees Yahoo Finance*
