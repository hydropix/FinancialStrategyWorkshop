# Guide de Publication du Wiki

Ce document explique comment publier la documentation wiki sur GitHub.

## Prérequis

1. **Repo public** : Le wiki GitHub gratuit nécessite un repo public
2. **Git installé** : https://git-scm.com/download/win
3. **Wiki activé** : Sur GitHub, allez dans Settings > Wiki > Enable

---

## Méthode 1 : Automatique (Recommandée)

### Étape 1 : Vérifier que le wiki est activé

Sur GitHub :
1. Allez sur votre repo `FinancialStrategyWorkshop`
2. Cliquez sur **Settings** (en haut à droite)
3. Dans le menu de gauche, cliquez sur **Wiki**
4. Cochez **"Restrict editing to collaborators only"** (optionnel, mais recommandé)
5. Cliquez sur **Save**

### Étape 2 : Lancer le script

Dans PowerShell (dans le dossier du projet) :

```powershell
# Option 1: Avec vos identifiants
.\publish_wiki.ps1 -Username "votre_username"

# Option 2: Par défaut (hydropix)
.\publish_wiki.ps1
```

Le script va :
1. ✅ Vérifier que Git est installé
2. ✅ Commit les fichiers wiki dans le repo principal (backup)
3. ✅ Cloner le repo wiki séparé (`FinancialStrategyWorkshop.wiki.git`)
4. ✅ Copier les fichiers
5. ✅ Push sur GitHub

### Étape 3 : Vérifier

Allez sur : `https://github.com/votre_username/FinancialStrategyWorkshop/wiki`

Vous devriez voir :
- Une page d'accueil avec le TL;DR
- Un menu de navigation sur la droite
- Tous les graphiques affichés

---

## Méthode 2 : Manuelle (Si l'automatique échoue)

Si le script automatique ne fonctionne pas (problème de droits, etc.), utilisez cette méthode :

### Étape 1 : Lancer le script simple

```powershell
.\publish_wiki_simple.ps1 -Username "votre_username"
```

Ce script va :
- Créer un zip avec tous les fichiers wiki
- Ouvrir le dossier dans l'explorateur
- Ouvrir l'URL du wiki dans votre navigateur

### Étape 2 : Créer les pages manuellement

Sur GitHub :
1. Allez sur l'onglet **Wiki**
2. Cliquez sur **"Create the first page"**
3. Titre : `Home`
4. Copiez-collez le contenu de `wiki/Home.md`
5. Cliquez sur **Save**

Répétez pour chaque page :
- `Home` → Contenu de `wiki/Home.md`
- `Resultats-Detailles` → Contenu de `wiki/Resultats-Detailles.md`
- `Graphiques` → Contenu de `wiki/Graphiques.md`
- `Methodologie` → Contenu de `wiki/Methodologie.md`
- `Conclusions` → Contenu de `wiki/Conclusions.md`
- `References` → Contenu de `wiki/References.md`

---

## Résolution des Problèmes

### Erreur : "Impossible de cloner le wiki"

**Cause** : Le wiki n'est pas encore initialisé sur GitHub.

**Solution** :
1. Créez manuellement la première page via l'interface web
2. Supprimez le dossier `FinancialStrategyWorkshop.wiki.git` s'il existe
3. Relancez le script

### Erreur : "Permission denied"

**Cause** : Problème d'authentification Git.

**Solution** :
```powershell
# Configurer Git
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"

# Se connecter à GitHub
git credential-manager login
```

### Les images ne s'affichent pas

**Cause** : Les graphiques ne sont pas encore sur la branche `main`.

**Solution** :
```powershell
git add charts/
git commit -m "Ajout des graphiques pour le wiki"
git push origin main
```

Attendez 1-2 minutes que GitHub mette à jour les URLs des images brutes.

---

## Structure du Wiki Publié

Une fois publié, votre wiki aura cette structure :

```
FinancialStrategyWorkshop.wiki/
├── Home.md                    # Page d'accueil
├── Resultats-Detailles.md     # Analyses complètes
├── Graphiques.md              # Tous les graphiques
├── Methodologie.md            # Comment reproduire
├── Conclusions.md             # Leçons apprises
└── References.md              # Papers et livres
```

---

## Mise à Jour du Wiki

Pour mettre à jour le wiki après des modifications :

```powershell
# Méthode automatique
.\publish_wiki.ps1

# Le script detectera les changements et poussera uniquement si nécessaire
```

---

## URLs Importantes

| Ressource | URL |
|-----------|-----|
| **Wiki** | `https://github.com/votre_username/FinancialStrategyWorkshop/wiki` |
| **Repo** | `https://github.com/votre_username/FinancialStrategyWorkshop` |
| **Settings** | `https://github.com/votre_username/FinancialStrategyWorkshop/settings` |
| **Wiki Settings** | `https://github.com/votre_username/FinancialStrategyWorkshop/settings/wiki` |

---

## Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. Vérifiez que le repo est bien **public**
2. Vérifiez que le wiki est bien **activé** dans Settings
3. Essayez la méthode manuelle (Méthode 2)
4. Consultez la documentation GitHub : https://docs.github.com/en/communities/documenting-your-project-with-wikis

---

**Date** : 2026-02-14
