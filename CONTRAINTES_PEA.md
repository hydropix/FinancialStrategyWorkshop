# Contraintes PEA - Diversification Geographique

## Qu'est-ce qu'un PEA ?

Le Plan d'Epargne en Actions (PEA) est un enveloppe fiscale francaise qui permet d'investir en actions avec des avantages fiscaux apres 5 ans :
- Pas d'impot sur les plus-values (hors prelevements sociaux 17.2%)
- Exoneration d'impot sur le revenu apres 5 ans

**MAIS avec des contraintes strictes sur les actifs eligibles.**

---

## Contraintes Principales du PEA

### 1. Geographique - Union Europeenne uniquement

**Regle :** Seules les societes ayant leur siege fiscal dans l'**UE** sont eligibles.

| Region | Eligible PEA ? | Explication |
|--------|----------------|-------------|
| **France** | ✅ Oui | Siège en France |
| **Allemagne** | ✅ Oui | Siège en Allemagne |
| **Pays-Bas** | ✅ Oui | Siège aux Pays-Bas |
| **Irlande** | ✅ Oui | Siège en Irlande |
| **Royaume-Uni** | ❌ **Non** | Brexit - Plus dans l'UE |
| **Suisse** | ❌ **Non** | Hors UE |
| **Etats-Unis** | ❌ **Non** | Hors UE |
| **Japon** | ❌ **Non** | Hors UE |
| **Emergents** | ❌ **Non** | Hors UE |

### 2. Type d'Actifs

**Eligibles :**
- ✅ Actions de societes europeennes
- ✅ OPCVM (fonds d'investissement) detenant >75% d'actions europeennes
- ✅ ETF cotes eligibles au PEA

**Non eligibles :**
- ❌ Obligations
- ❌ Matieres premieres
- ❌ Crypto
- ❌ ETF monde (trop d'actifs non-UE)

---

## ETF Disponibles en PEA

### ETF Monde/Developpes (avec contrainte UE)

| ETF | Compartiment | TER | Exposition reelle |
|-----|--------------|-----|-------------------|
| **CW8** (Amundi MSCI World) | ✅ PEA | 0.18% | ~65% US + 35% Europe/Japon |
| **EUNL** (iShares Core MSCI World) | ❌ **Non PEA** | 0.20% | Irlande - Non eligible |
| **EWLD** (Amundi MSCI World) | ✅ PEA | 0.18% | Equivalent CW8 |

**Probleme :** Ces ETF "Monde" contiennent ~65% d'actions US (Apple, Microsoft, etc.) qui sont **societes americaines**, donc **non eligibles au PEA** en theorie...

**Mais :** L'ETF lui-meme est francais/americain cote en Europe, donc il y a une tolerance. Cependant, ce n'est pas la vraie diversification recherchee.

### ETF Europe (100% PEA)

| ETF | Indice | TER | Composition |
|-----|--------|-----|-------------|
| **CEU** (Amundi STOXX 600) | STOXX 600 | 0.25% | 600 plus grandes entreprises europeennes |
| **EZE** (iShares Euro STOXX 50) | EURO STOXX 50 | 0.20% | 50 leaders zone euro |
| **EXV1** (iShares STOXX 600) | STOXX 600 | 0.20% | Alternative a CEU |

**Avantage :** 100% eligible PEA
**Inconvenient :** Concentration Europe uniquement

### ETF Par Pays (PEA)

| Pays | ETF | Disponible PEA ? |
|------|-----|------------------|
| France | CAC 40 (AMST) | ✅ Oui |
| Allemagne | DAX (EXS1) | ✅ Oui |
| Espagne | IBEX (IBEX) | ✅ Oui |
| Italie | FTSE MIB (IT40) | ✅ Oui |

---

## Le Probleme du Japon et des Emergents

### ❌ Japon - NON disponible en PEA

Les ETF Japon (EWJ, IJPA) sont :
- Soit americains (iShares US)
- Soit irlandais (UCITS)
- **Aucun ETF Japon francais eligible PEA**

**Consequence :** Impossible d'avoir la meilleure diversification (Japon correl 0.72 avec US) dans un PEA.

### ❌ Marchés Emergents - NON disponibles en PEA

Les ETF EM (EEM, EMIM, VWO) sont :
- Domiciilies en Irlande ou US
- Investissent en Chine, Bresil, Inde...
- **Non eligibles au PEA**

---

## Solutions pour le PEA

### Option 1 : PEA "Pur" (100% eligible)

**Allocation possible :**
```
60% CW8  (Amundi MSCI World)  - Indirectement 40% US + 20% Europe/Japon
40% CEU  (Amundi STOXX 600)  - 100% Europe
```

**Problemes :**
- CW8 contient indirectement des actions US (non eligibles theoriquement)
- Pas de vraie diversification (Japon, EM)
- Exposition US inevitable (~40% via CW8)

### Option 2 : PEA + CTO Complementaire (Recommande)

**PEA (Fiscalite optimale) :**
```
100% CW8  (ou mix CW8 + CEU)
```
*Limite : 150 000€ de versement*

**CTO (Compte-Titre Ordinaire) - Diversification :**
```
Pour l'excedent ou la diversification internationale :
- CSPX (S&P 500) 
- IJPA (Japon)
- EMIM (Emergents)
- EXV1 (Europe si pas en PEA)
```

### Option 3 : PEA avec Selection d'Actions

**Alternative :** Acheter directement des actions europeennes etrangeres

**Exemple de portefeuille actions PEA :**
```
40% Actions francaises (TotalEnergies, LVMH, Sanofi...)
30% Actions europeennes via PEA (Siemens, SAP, ASML...)
30% CW8 (diversification supplementaire)
```

**Inconvenient :** Gestion active, temps, frais de transaction plus eleves

---

## Comparaison PEA vs CTO pour la Diversification

| Critere | PEA Seul | PEA + CTO | CTO Seul |
|---------|----------|-----------|----------|
| **Diversification Japon** | ❌ Impossible | ✅ Possible | ✅ Possible |
| **Diversification EM** | ❌ Impossible | ✅ Possible | ✅ Possible |
| **Reduction risque US** | ❌ Limite (~40% min) | ✅ Oui (20-30%) | ✅ Oui (30-35%) |
| **Fiscalite** | ✅ Excellente | ✅ Bonne | ⚠️ Standard |
| **Simplicite** | ✅ Simple | ⚠️ 2 comptes | ✅ Simple |
| **Plafond** | 150 000€ | Illimite | Illimite |

---

## Recommandation Pratique

### Si vous avez moins de 150 000€ a investir

**PEA uniquement :**
```
60% CW8  (Amundi MSCI World)  
40% CEU  (Amundi STOXX 600 Europe)
```

**Acceptez :**
- Une exposition US inevitable (~25% via CW8)
- Pas de Japon dedie
- Pas d'EM
- Fiscalite optimisee

### Si vous avez plus de 150 000€

**PEA (150k€ max) :**
```
100% CW8
```

**CTO (excedent) :**
```
35% CSPX (US)
25% EXV1 (Europe)
20% EMIM (EM)
15% IJPA (Japon)  <- La cle pour la diversification !
5%  ITPA (Pacifique)
```

### Si vous voulez vraiment reduire le risque US avec un PEA

**Malheureusement... c'est impossible.**

Le PEA force une exposition minimum de ~25-40% aux US (via les ETF monde), et interdit :
- Le Japon (meilleure diversification)
- Les EM (rendement/croissance)

**Alternative :** Accepter la fiscalite standard et utiliser un CTO pour la vraie diversification.

---

## ETF PEA Disponibles - Liste Complete

### Distributeurs principaux
- **Amundi** (CW8, CEU) - Francais, 100% PEA
- **Lyxor** (certaines series) - Francais
- **BNP Paribas** - Francais

### ETF a eviter en PEA
- iShares (EUNL, EXV1) - Souvent irlandais
- Vanguard - Irlandais
- Xtrackers - Irlandais

**Verifier toujours :** Le "compartiment" doit etre "Eligibilite PEA : OUI"

---

## Exemple de Recherche d'ETF PEA

### Etape 1 : Verifier le domicile
- ✅ Domicile = France, Luxembourg (certain cas)
- ❌ Domicile = Irlande, US

### Etape 2 : Verifier l'indice
- ✅ Indice Europe ou Monde avec >75% UE
- ❌ Indice US, Japon, EM pur

### Etape 3 : Verifier la composition
- CW8 = 65% US + 35% Europe/Japon (acceptable)
- CEU = 100% Europe (optimal)

---

## Conclusion

### Le PEA est-il compatible avec la diversification geographique optimale ?

**Reponse : NON completement.**

Le PEA interdit :
- ❌ Japon (meilleure diversification vs US)
- ❌ Marchés Emergents (croissance)
- ❌ Asie Pacifique (ex-Japon)

Le PEA force :
- ⚠️ Minimum ~25-40% d'exposition US (via ETF monde)

### Solution recommandee

**Pour les petits montants (<50k€) :**
- PEA avec CW8 uniquement
- Accepter la concentration US

**Pour les montants moyens (50-150k€) :**
- PEA : 60% CW8 + 40% CEU
- Maximiser l'Europe, minimiser l'US indirect

**Pour les gros montants (>150k€) :**
- PEA : 150k€ en CW8 (fiscalite)
- CTO : Diversification complete avec Japon/EM

---

**Date :** 2026-02-14  
**Important :** Verifier toujours l'eligibilite PEA avant achat, les regles evoluent.
