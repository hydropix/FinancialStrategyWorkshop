#!/usr/bin/env powershell
# Script de publication automatique du Wiki GitHub
# Usage: .\publish_wiki.ps1

param(
    [string]$Username = "hydropix",
    [string]$RepoName = "FinancialStrategyWorkshop"
)

$ErrorActionPreference = "Stop"
$WikiRepo = "$RepoName.wiki.git"
$WikiUrl = "https://github.com/$Username/$WikiRepo"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Publication du Wiki GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repo principal: $RepoName" -ForegroundColor Yellow
Write-Host "Repo wiki: $WikiRepo" -ForegroundColor Yellow
Write-Host ""

# Verifier que git est installe
try {
    $gitVersion = git --version
    Write-Host "[OK] Git detecte: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Git non trouve. Installez Git: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Verifier que le dossier wiki existe
if (-not (Test-Path "wiki")) {
    Write-Host "[ERREUR] Dossier 'wiki' non trouve. Executez d'abord le script Python." -ForegroundColor Red
    exit 1
}

# Obtenir le chemin absolu
$ProjectPath = Get-Location
$ParentPath = Split-Path -Parent $ProjectPath
$WikiPath = Join-Path $ParentPath $WikiRepo

Write-Host "[OK] Dossier wiki trouve" -ForegroundColor Green
Write-Host "Chemin projet: $ProjectPath" -ForegroundColor Gray
Write-Host ""

# Etape 1: Commit les fichiers wiki dans le repo principal (backup)
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Etape 1: Backup dans le repo principal" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

try {
    git add wiki/
    $status = git status --porcelain
    if ($status) {
        git commit -m "Ajout fichiers wiki complets"
        git push origin main
        Write-Host "[OK] Fichiers wiki commites et pousses sur main" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Pas de changements a commiter (deja a jour)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[AVERTISSEMENT] Impossible de pousser sur main: $_" -ForegroundColor Yellow
}

# Etape 2: Cloner le repo wiki s'il n'existe pas
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Etape 2: Clone du repo wiki" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if (Test-Path $WikiPath) {
    Write-Host "[INFO] Le repo wiki existe deja: $WikiPath" -ForegroundColor Yellow
    Write-Host "Mise a jour..." -ForegroundColor Yellow
    Set-Location $WikiPath
    git pull origin master
} else {
    Write-Host "Clonage depuis $WikiUrl..." -ForegroundColor Yellow
    Set-Location $ParentPath
    try {
        git clone $WikiUrl
        Write-Host "[OK] Repo wiki clone" -ForegroundColor Green
    } catch {
        Write-Host "[ERREUR] Impossible de cloner le wiki. Verifiez que:" -ForegroundColor Red
        Write-Host "  1. Le repo est public" -ForegroundColor Red
        Write-Host "  2. L'onglet Wiki est active sur GitHub" -ForegroundColor Red
        Write-Host "  3. Vous avez les droits d'ecriture" -ForegroundColor Red
        Write-Host ""
        Write-Host "Alternative: Utilisez l'interface web pour creer la premiere page du wiki," -ForegroundColor Yellow
        Write-Host "puis relancez ce script." -ForegroundColor Yellow
        exit 1
    }
}

# Etape 3: Copier les fichiers
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Etape 3: Copie des fichiers wiki" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Supprimer les anciens fichiers (sauf .git)
Get-ChildItem -Path $WikiPath -File | Remove-Item -Force
Write-Host "[OK] Anciens fichiers supprimes" -ForegroundColor Green

# Copier les nouveaux fichiers
Copy-Item -Path "$ProjectPath\wiki\*" -Destination $WikiPath -Recurse -Force
Write-Host "[OK] Nouveaux fichiers copies" -ForegroundColor Green

# Lister les fichiers
Write-Host ""
Write-Host "Fichiers dans le wiki:" -ForegroundColor Gray
Get-ChildItem -Path $WikiPath -File | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor Gray
}

# Etape 4: Commit et push
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Etape 4: Publication sur GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location $WikiPath

try {
    git add .
    $status = git status --porcelain
    
    if ($status) {
        git commit -m "Mise a jour wiki - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        git push origin master
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "[SUCCES] Wiki publie avec succes!" -ForegroundColor Green
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "URL du wiki:" -ForegroundColor Cyan
        Write-Host "https://github.com/$Username/$RepoName/wiki" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "[INFO] Pas de changements a publier" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERREUR] Impossible de publier: $_" -ForegroundColor Red
    exit 1
}

# Retour au dossier projet
Set-Location $ProjectPath
Write-Host "Termine." -ForegroundColor Green
