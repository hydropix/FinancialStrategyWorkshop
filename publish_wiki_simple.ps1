#!/usr/bin/env powershell
# Script simple de publication du Wiki (methode manuelle via zip)
# A utiliser si la methode git clone ne fonctionne pas

param(
    [string]$Username = "hydropix"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Publication Wiki - Methode Manuelle" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Creer le zip
$ZipFile = "wiki_export.zip"
$WikiPath = "wiki"

if (-not (Test-Path $WikiPath)) {
    Write-Host "[ERREUR] Dossier 'wiki' non trouve!" -ForegroundColor Red
    exit 1
}

Write-Host "Creation de l'archive..." -ForegroundColor Yellow
if (Test-Path $ZipFile) {
    Remove-Item $ZipFile
}

Compress-Archive -Path "$WikiPath\*" -DestinationPath $ZipFile -Force
Write-Host "[OK] Archive cree: $ZipFile" -ForegroundColor Green
Write-Host ""

# 2. Instructions
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Instructions pour publier sur GitHub:" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Allez sur: https://github.com/$Username/FinancialStrategyWorkshop/wiki" -ForegroundColor White
Write-Host ""
Write-Host "2. Cliquez sur 'Create the first page'" -ForegroundColor White
Write-Host ""
Write-Host "3. Creez les pages suivantes:" -ForegroundColor Yellow
Write-Host "   - Home (copiez le contenu de Home.md)" -ForegroundColor Gray
Write-Host "   - Resultats-Detailles" -ForegroundColor Gray
Write-Host "   - Graphiques" -ForegroundColor Gray
Write-Host "   - Methodologie" -ForegroundColor Gray
Write-Host "   - Conclusions" -ForegroundColor Gray
Write-Host "   - References" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Les fichiers source sont dans: $((Get-Location).Path)\$WikiPath\" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour ouvrir le dossier..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Ouvrir l'explorateur
explorer (Get-Location).Path

# Ouvrir le navigateur
Start-Process "https://github.com/$Username/FinancialStrategyWorkshop/wiki"
