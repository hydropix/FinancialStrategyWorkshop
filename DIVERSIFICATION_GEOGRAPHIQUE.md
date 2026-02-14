# Diversification Géographique - Réduction du Risque US

## Contexte

L'exposition exclusive aux marchés US présente des risques spécifiques:
- Concentration sectorielle (Tech = ~30% du S&P 500)
- Valuations élevées comparées aux autres marchés
- Incertitudes politiques (tarifs Trump, politique monétaire)
- Dollar US comme risque de change

## Objectif

Proposer des stratégies d'allocation géographique qui:
1. Réduisent la dépendance aux US
2. Maintiennent une croissance solide
3. Bénéficient de la diversification
4. Sont simples à implémenter avec des ETF

---

## 1. Univers d'ETF Géographiques Disponibles

| Région | ETF Exemple | Ticker | Frais | Exposition |
|--------|-------------|--------|-------|------------|
| **Monde** | iShares MSCI World | URTH / IWDA | 0.20% | 70% US + 30% Intl |
| **US** | SPDR S&P 500 | SPY | 0.09% | S&P 500 |
| **Europe** | iShares STOXX 600 | IUSE / EXV1 | 0.20% | Europe développée |
| **EM** | iShares MSCI EM | EEM | 0.68% | Marchés émergents |
| **Japon** | iShares MSCI Japan | EWJ | 0.50% | Japon |
| **Chine** | iShares MSCI China | MCHI | 0.59% | Chine A-Shares + H-Shares |
| **Pacifique** | iShares MSCI Pacific | EPP | 0.50% | Japon + Australie + HK |

---

## 2. Stratégies Proposées

### A. Buy & Hold Diversifié (Base)

**Allocation équilibrée non-US:**
```
40% Monde (MSCI World) - inclut US mais diversifié
25% Europe (STOXX 600)
15% Marchés Emergents
10% Japon
10% Pacifique ex-Japon
```

**Avantages:**
- Simple, pas de rebalancement actif
- Frais minimaux
- Exposition US réduite à ~30% via MSCI World

**Inconvénients:**
- Pas de surperformance potentielle
- Risque de change non couvert

---

### B. Rotation Géographique par Momentum

**Principe:** Sélectionner les 2-3 meilleures régions selon leur momentum sur 6-12 mois.

**Univers:** 5-6 ETF régionaux
**Rebalancement:** Trimestriel
**Lookback:** 6-12 mois

**Avantages:**
- Capture les tendances régionales
- Peut éviter les marchés en difficulté
- Historiquement efficace sur les marchés

**Risques:**
- Whipsaw en période de volatilité
- Frais de transaction plus élevés

---

### C. Strategie "Risk Parity" Géographique

**Principe:** Allouer l'inverse de la volatilité de chaque région.

```
Poids_region = (1/Volatilite_region) / Somme(1/Volatilite)
```

**Rebalancement:** Mensuel
**Lookback volatilité:** 3-6 mois

**Avantages:**
- Réduit l'impact des régions volatiles (EM)
- Portefeuille plus stable
- Bon ratio de Sharpe

---

### D. Allégement Conditionnel US

**Principe:** Réduire l'exposition US quand signaux faibles.

**Signaux d'allégement:**
- Momentum US < momentum World sur 6 mois
- Volatilité US > 150% de la moyenne
- Inversion curve (si données dispo)

**Allocation dynamique:**
```
US_Normal = 50%
US_Reduit = 20% (réalloué vers Europe + EM)
```

---

### E. Couverture Devise Dynamique

**Principe:** Alterner entre ETF couvert/non-couvert selon tendance du dollar.

**Règle simple:**
- Dollar fort (momentum USD positif) → ETF couverts en EUR
- Dollar faible → ETF non-couverts

---

## 3. Analyse des Corrélations Historiques

### Corrélations typiques (données mensuelles)

| | US | Europe | EM | Japon |
|---|----|--------|-----|-------|
| **US** | 1.00 | 0.85 | 0.75 | 0.65 |
| **Europe** | 0.85 | 1.00 | 0.70 | 0.60 |
| **EM** | 0.75 | 0.70 | 1.00 | 0.55 |
| **Japon** | 0.65 | 0.60 | 0.55 | 1.00 |

**Constats:**
- Corrélations élevées en période de stress (tous marchés baissent ensemble)
- Japon offre la meilleure diversification
- EM = plus volatile mais corrélations modérées

### Périodes de Découplage

| Période | Marché Outperformant | Commentaire |
|---------|---------------------|-------------|
| 2000-2003 | Europe, EM | Bulle Internet US |
| 2003-2007 | EM, Commodities | Super cycle matières |
| 2010-2012 | US | Crise dette européenne |
| 2018 | US | Guerre commerciale |
| 2022 | Energie/Europe | Guerre Ukraine |

---

## 4. Backtesting - Scénarios à Tester

### Scénario 1: Momentum Multi-Régions
```python
Univers: [SPY, IUSE, EEM, EWJ, EPP]
Lookback: 12 mois
Top: 2 meilleurs momentum
Rebalancement: Trimestriel
```

### Scénario 2: Risk Parity
```python
Univers: [SPY, IUSE, EEM, EWJ]
Volatilité: 3 mois rolling
Poids: Inverse de la vol
Rebalancement: Mensuel
```

### Scénario 3: Mixte US/Non-US Dynamique
```python
Signal: Momentum US vs Momentum World
Si US > World: 60% US, 40% Intl
Si US < World: 30% US, 70% Intl
Intl = Equal weight Europe + EM + Japon
```

---

## 5. Implémentation Pratique

### Avec ETF Européens (UCITS)

| Stratégie | ETF Recommandés | Courtier |
|-----------|-----------------|----------|
| Monde | CW8 (Amundi), SWDA (iShares) | PEA/CTO |
| Europe | EXV1 (iShares), CEU (Amundi) | PEA/CTO |
| EM | AEM (Amundi), EMIM (iShares) | PEA/CTO |
| Japon | JPN (iShares) | CTO |

### Frais Totaux Estimés

| Stratégie | Frais ETF | Transactions/an | Frais Total |
|-----------|-----------|-----------------|-------------|
| Buy & Hold | 0.25% | 1 | 0.25% |
| Momentum Trim. | 0.35% | 4 | 0.50% |
| Risk Parity | 0.30% | 12 | 0.80% |

---

## 6. Risques Spécifiques par Région

| Région | Risques Actuels (2025) |
|--------|------------------------|
| **US** | Tarifs Trump, récession tech, dette élevée |
| **Europe** | Guerre Ukraine, energie, fragmentation politique |
| **EM** | Chine (immobilier), forte volatilité |
| **Japon** | Yen faible, démographie |

---

## 7. Prochaines Étapes

1. **Télécharger les données** historiques des ETF régionaux
2. **Backtester** les stratégies A, B, C sur 2007-2024
3. **Analyser** les périodes de crise (2008, 2020, 2022)
4. **Optimiser** les paramètres (lookback, fréquence)
5. **Tester** avec frais réels et glissements

---

## Références

- [Asness et al., 2013] Value and Momentum Everywhere
- [Blitz & Vliet, 2008] Global Tactical Cross-Asset Allocation
- [MSCI Annual Reports] Poids géographiques historiques
