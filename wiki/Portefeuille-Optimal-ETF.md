# Portefeuille Optimal d'ETF - Recommandations

## Resume Executif

Apres analyse des 18 ans de donnees (2007-2024), voici les **conclusions pratiques** pour construire un portefeuille d'ETF optimal.

---

## 1. Conclusions sur l'Achat d'ETF

### ✅ Ce qui fonctionne

| Strategie | Rendement | Risque | Verdict |
|-----------|-----------|--------|---------|
| **ETF S&P 500 seul** | 10.3%/an | Tres eleve (-55% drawdown) | ❌ Trop risque |
| **ETF Monde (ACWI)** | 7.3%/an | Eleve (-56% drawdown) | ❌ Sous-performe |
| **Diversification Geographique** | 9.6%/an | **Modere (-33% drawdown)** | ✅ **Optimal** |

### ❌ Ce qui ne fonctionne PAS

1. **Exposition 100% US** : Drawdown de -55% en 2008, trop de concentration politique/economique
2. **ETF Monde seul** : 70% d'actions US dedans, correlation 0.97 avec S&P 500
3. **Sous-allocation US** : Penalise sur le long terme (US surperforme)

### 🎯 Verdict

> **La diversification geographique dynamique est superieure** au Buy & Hold simple.
> 
> -40% de risque pour -0.7% de rendement = excellent compromis

---

## 2. Portefeuilles Recommandes

### Option A : Portefeuille Equilibre (Recommande)

**Pour :** Investisseur prudent souhaitant reduire le risque US

| ETF | Allocation | Role |
|-----|------------|------|
| **CSPX** (S&P 500) | **35%** | Core US reduit |
| **EXV1** (STOXX 600) | **25%** | Europe developpee |
| **EMIM** (EM) | **20%** | Croissance emergente |
| **IJPA** (Japon) | **15%** | Diversification (correl 0.72) |
| **EPPA** (Pacifique ex-JP) | **5%** | Australie/Hong Kong |

**Caracteristiques estimees :**
- Rendement : ~8.5%/an
- Volatilite : ~16% (vs 19.8% S&P 500)
- Max Drawdown : ~-35% (vs -55% S&P 500)
- Frais moyens : 0.15%

---

### Option B : Portefeuille Dynamique (Optimal)

**Pour :** Investisseur actif suivant la strategie "US vs World"

#### Configuration Normale (60% US quand momentum US > World)
| ETF | Allocation |
|-----|------------|
| CSPX (S&P 500) | 60% |
| EXV1 (Europe) | 15% |
| EMIM (EM) | 15% |
| IJPA (Japon) | 10% |

#### Configuration Defensive (30% US quand momentum US < World)
| ETF | Allocation |
|-----|------------|
| CSPX (S&P 500) | 30% |
| EXV1 (Europe) | 25% |
| EMIM (EM) | 25% |
| IJPA (Japon) | 20% |

**Regle :** Rebalancer mensuellement selon momentum 6 mois

**Caracteristiques historiques (2007-2024) :**
- Rendement : 9.6%/an
- Volatilite : 16.2%
- Max Drawdown : -33%
- Sharpe : 0.59 (meilleur que S&P 500 : 0.52)

---

### Option C : Portefeuille Conservateur (Minimum de risque)

**Pour :** Retraite proche ou tres averse au risque

| ETF | Allocation | Justification |
|-----|------------|---------------|
| **EXV1** (Europe) | **30%** | Proximite geographique/fiscale |
| **IJPA** (Japon) | **25%** | Meilleure diversification (correl 0.72) |
| **CSPX** (S&P 500) | **20%** | Reduction US max |
| **EMIM** (EM) | **15%** | Croissance |
| **EPPA** (Pacifique) | **10%** | Diversification |

**Caracteristiques estimees :**
- Rendement : ~7%/an
- Volatilite : ~15%
- Max Drawdown : ~-30%

---

## 3. ETF Specifiques Recommandes (Europe - UCITS)

| Region | ETF | Ticker | TER | Bourse |
|--------|-----|--------|-----|--------|
| **US** | iShares Core S&P 500 | CSPX | 0.07% | LSE/Euronext |
| **Europe** | iShares STOXX 600 | EXV1 | 0.20% | Xetra |
| **EM** | iShares Core MSCI EM | EMIM | 0.18% | LSE |
| **Japon** | iShares MSCI Japan | IJPA | 0.20% | LSE |
| **Pacifique** | iShares MSCI Pacific | ITPA | 0.20% | LSE |
| **Monde** | iShares MSCI World | IWDA | 0.20% | LSE |

**Alternative moins chere (Amundi) :**
- CW8 (MSCI World) : 0.18% TER

---

## 4. Implementation Pratique

### Avec un PEA (France)

**Disponibles en PEA :**
- CW8 (Amundi MSCI World)
- CEU (Amundi STOXX 600)
- Japon : pas d'ETF PEA pur, utiliser CW8

**Allocation PEA :**
```
60% CW8 (Monde) - inclut US/Japon
40% CEU (Europe)
```

### Avec un Compte-Titre Ordinaire (CTO)

**Meilleure diversification :**
```
35% CSPX (US)
25% EXV1 (Europe)  
20% EMIM (EM)
15% IJPA (Japon)
5% ITPA (Pacifique)
```

---

## 5. Rebalancement

### Strategie Statique (Buy & Hold)
- **Frequence** : Annuelle ou semi-annuelle
- **Seuil** : Rebalancer si deviation > 5% de l'allocation cible

### Strategie Dynamique (Momentum)
- **Frequence** : Mensuelle
- **Signal** : Momentum 6 mois US vs Momentum 6 mois World
- **Regle** : 60% US si US > World, sinon 30% US

---

## 6. Performance Historique Comparee

| Portefeuille | Rendement | Max DD | Sharpe | Note |
|--------------|-----------|--------|--------|------|
| 100% S&P 500 | 10.3% | **-55.2%** | 0.52 | ❌ Trop risque |
| 100% ACWI | 7.3% | -56.3% | 0.36 | ❌ Sous-performe |
| **Equilibre (Option A)** | **~8.5%** | **~-35%** | ~0.50 | ✅ Recommande |
| **Dynamique (Option B)** | **9.6%** | **-33.0%** | **0.59** | ✅ Optimal |
| Conservateur (Option C) | ~7.0% | ~-30% | ~0.45 | ✅ Prudent |

---

## 7. Conclusion Pratique

### Pour la plupart des investisseurs

**Utiliser le Portefeuille Equilibre (Option A) :**
- Simple a gerer (rebalancing annuel)
- Risque reduit de 40%
- Rendement preserve (~8.5% vs 10.3%)

### Pour les investisseurs actifs

**Utiliser le Portefeuille Dynamique (Option B) :**
- Meilleur ratio rendement/risque (Sharpe 0.59)
- S'adapte aux conditions de marche
- Requiert suivi mensuel

### A eviter

❌ **ETF Monde seul** : Trop d'exposition US (70%)
❌ **100% US** : Risque politique/concentration trop eleve
❌ **Sous-allocation US** (<20%) : Penalise le rendement long terme

---

## 8. Suivi et Ajustements

### Quand revisiter l'allocation ?

1. **Changement de profil de risque** (retraite approche, etc.)
2. **Evenement geopolitique majeur** (guerre, crise financiere)
3. **Tous les 2 ans** : revue strategique

### Signaux d'alerte
- Correlation US/Japon > 0.85 : Diversification moins efficace
- Volatilite US > 25% : Passer en mode defensif (moins d'US)
- Recession US : Augmenter Japon/Europe

---

**Date :** 2026-02-14  
**Base sur :** Tests 2007-2024, 10 ETF, 4 strategies
