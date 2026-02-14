"""
Script de visualisation des resultats Monte Carlo
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Creer le dossier pour les graphiques
os.makedirs('charts', exist_ok=True)

# Charger les resultats
results = pd.read_csv('data/monte_carlo_results.csv')

# Configuration des graphiques
plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Analyse Monte Carlo - Strategie Random + Stop-Loss (n=50)', fontsize=14, fontweight='bold')

# 1. Distribution des rendements totaux
ax1 = axes[0, 0]
n, bins, patches = ax1.hist(results['total_return'], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
ax1.axvline(results['total_return'].mean(), color='red', linestyle='--', linewidth=2, label=f"Moyenne: {results['total_return'].mean():.1f}%")
ax1.axvline(results['total_return'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediane: {results['total_return'].median():.1f}%")
ax1.axvline(190.86, color='orange', linestyle='-', linewidth=2, label='Benchmark: 190.9%')
ax1.set_xlabel('Rendement Total (%)')
ax1.set_ylabel('Frequence')
ax1.set_title('Distribution des Rendements Totaux')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Distribution des ratios de Sharpe
ax2 = axes[0, 1]
ax2.hist(results['sharpe_ratio'], bins=15, color='forestgreen', edgecolor='black', alpha=0.7)
ax2.axvline(results['sharpe_ratio'].mean(), color='red', linestyle='--', linewidth=2, label=f"Moyenne: {results['sharpe_ratio'].mean():.2f}")
ax2.axvline(results['sharpe_ratio'].median(), color='blue', linestyle='--', linewidth=2, label=f"Mediane: {results['sharpe_ratio'].median():.2f}")
ax2.set_xlabel('Ratio de Sharpe')
ax2.set_ylabel('Frequence')
ax2.set_title('Distribution des Ratios de Sharpe')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Distribution des Max Drawdown
ax3 = axes[1, 0]
ax3.hist(results['max_drawdown'], bins=15, color='coral', edgecolor='black', alpha=0.7)
ax3.axvline(results['max_drawdown'].mean(), color='red', linestyle='--', linewidth=2, label=f"Moyenne: {results['max_drawdown'].mean():.1f}%")
ax3.axvline(results['max_drawdown'].median(), color='blue', linestyle='--', linewidth=2, label=f"Mediane: {results['max_drawdown'].median():.1f}%")
ax3.set_xlabel('Max Drawdown (%)')
ax3.set_ylabel('Frequence')
ax3.set_title('Distribution des Drawdowns Maximaux')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Scatter: Rendement vs Risque (Drawdown)
ax4 = axes[1, 1]
scatter = ax4.scatter(results['max_drawdown'], results['total_return'], 
                      c=results['sharpe_ratio'], cmap='viridis', s=80, alpha=0.7, edgecolors='black')
ax4.set_xlabel('Max Drawdown (%)')
ax4.set_ylabel('Rendement Total (%)')
ax4.set_title('Rendement vs Risque (couleur = Sharpe)')
cbar = plt.colorbar(scatter, ax=ax4)
cbar.set_label('Ratio de Sharpe')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/monte_carlo_analysis.png', dpi=150, bbox_inches='tight')
print("Graphique sauvegarde: charts/monte_carlo_analysis.png")

# Creer un deuxieme graphique: Boxplots
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Boxplots des Metriques - Monte Carlo (n=50)', fontsize=14, fontweight='bold')

# Boxplot rendements
axes2[0].boxplot(results['total_return'], vert=True, patch_artist=True,
                 boxprops=dict(facecolor='steelblue', alpha=0.7))
axes2[0].set_ylabel('Rendement Total (%)')
axes2[0].set_title('Rendement Total')
axes2[0].grid(True, alpha=0.3)
axes2[0].axhline(190.86, color='orange', linestyle='--', linewidth=2, label='Benchmark')
axes2[0].legend()

# Boxplot Sharpe
axes2[1].boxplot(results['sharpe_ratio'], vert=True, patch_artist=True,
                 boxprops=dict(facecolor='forestgreen', alpha=0.7))
axes2[1].set_ylabel('Ratio de Sharpe')
axes2[1].set_title('Ratio de Sharpe')
axes2[1].grid(True, alpha=0.3)

# Boxplot Drawdown
axes2[2].boxplot(results['max_drawdown'], vert=True, patch_artist=True,
                 boxprops=dict(facecolor='coral', alpha=0.7))
axes2[2].set_ylabel('Max Drawdown (%)')
axes2[2].set_title('Max Drawdown')
axes2[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/monte_carlo_boxplots.png', dpi=150, bbox_inches='tight')
print("Graphique sauvegarde: charts/monte_carlo_boxplots.png")

# Afficher les statistiques dans la console
print("\n" + "="*70)
print("STATISTIQUES DETAILLEES")
print("="*70)

for col in ['total_return', 'sharpe_ratio', 'max_drawdown']:
    print(f"\n{col.upper()}:")
    print(f"  Count:   {results[col].count():.0f}")
    print(f"  Mean:    {results[col].mean():.2f}")
    print(f"  Std:     {results[col].std():.2f}")
    print(f"  Min:     {results[col].min():.2f}")
    print(f"  25%:     {results[col].quantile(0.25):.2f}")
    print(f"  50%:     {results[col].median():.2f}")
    print(f"  75%:     {results[col].quantile(0.75):.2f}")
    print(f"  Max:     {results[col].max():.2f}")

print("\n" + "="*70)
print("Comparaison avec Benchmark (S&P 500 equipondere):")
print("="*70)
benchmark_return = 190.86
strategy_mean = results['total_return'].mean()
print(f"  Benchmark:        {benchmark_return:.2f}%")
print(f"  Strategie (moy):  {strategy_mean:.2f}%")
print(f"  Difference:       {strategy_mean - benchmark_return:.2f}%")
print(f"  % > Benchmark:    {(results['total_return'] > benchmark_return).mean() * 100:.1f}%")

# plt.show()  # Desactive pour sauvegarde automatique
