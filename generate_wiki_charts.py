#!/usr/bin/env python3
"""
Génération des graphiques pour le wiki GitHub
Synthèse visuelle de toutes les stratégies testées
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# Style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

def create_comparison_chart():
    """Graphique comparatif des stratégies"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Workshop Strategies Investissement - Resultats Complets', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # === GRAPHIQUE 1: Rendement US ===
    ax1 = axes[0, 0]
    strategies = ['Buy & Hold\nS&P 500', 'Random +\nStop-Loss', 'Momentum\n(Base)', 'Momentum\n(Optimal)']
    returns_us = [190.9, 123.0, 117.1, 376.3]
    colors1 = ['#2ecc71', '#e74c3c', '#e74c3c', '#27ae60']
    
    bars1 = ax1.bar(strategies, returns_us, color=colors1, edgecolor='black', linewidth=1.5)
    ax1.axhline(y=190.9, color='green', linestyle='--', linewidth=2, label='Benchmark S&P 500')
    ax1.set_ylabel('Rendement Total (%)', fontweight='bold')
    ax1.set_title('Marche US (2018-2024)', fontweight='bold', fontsize=12)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs
    for bar, val in zip(bars1, returns_us):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # === GRAPHIQUE 2: Rendement Europe ===
    ax2 = axes[0, 1]
    strategies_eu = ['Buy & Hold\nEURO STOXX', 'Momentum\n(Base)', 'Momentum\n(Optimal)']
    returns_eu = [441.5, 296.2, 243.8]
    colors2 = ['#2ecc71', '#e74c3c', '#e74c3c']
    
    bars2 = ax2.bar(strategies_eu, returns_eu, color=colors2, edgecolor='black', linewidth=1.5)
    ax2.axhline(y=441.5, color='green', linestyle='--', linewidth=2, label='Benchmark EURO STOXX')
    ax2.set_ylabel('Rendement Total (%)', fontweight='bold')
    ax2.set_title('Marche Europe (2010-2024)', fontweight='bold', fontsize=12)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars2, returns_eu):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # === GRAPHIQUE 3: Impact des frais (Momentum Optimal US) ===
    ax3 = axes[1, 0]
    fee_levels = ['0%', '0.1%', '0.2%', '0.5%', '1.0%']
    returns_with_fees = [376.3, 358.9, 350.3, 267.3, 236.3]
    
    bars3 = ax3.bar(fee_levels, returns_with_fees, color='#3498db', edgecolor='black', linewidth=1.5)
    ax3.axhline(y=190.9, color='red', linestyle='--', linewidth=2, label='Benchmark S&P 500')
    ax3.set_ylabel('Rendement Total (%)', fontweight='bold')
    ax3.set_xlabel('Frais de Transaction', fontweight='bold')
    ax3.set_title('Impact des Frais - Momentum Optimal (US)', fontweight='bold', fontsize=12)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars3, returns_with_fees):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # === GRAPHIQUE 4: Scorecard ===
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Tableau récapitulatif
    table_data = [
        ['Stratégie', 'US', 'Europe', 'Frais 0.5%'],
        ['Buy & Hold Indice', '✅ 191%', '✅ 442%', '✅ Bas'],
        ['Random + Stop-Loss', '❌ 123%', '❌ 353%', '✅ Modéré'],
        ['Momentum (Base)', '❌ 117%', '❌ 296%', '❌ Élevé'],
        ['Momentum (Optimal)', '✅ 376%', '❌ 244%', '⚠️ Très élevé'],
    ]
    
    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.2, 0.2, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    # Style header
    for i in range(4):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style lignes
    for i in range(1, 5):
        for j in range(4):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
    
    ax4.set_title('Tableau Comparatif', fontweight='bold', fontsize=12, pad=20)
    
    plt.tight_layout()
    plt.savefig('charts/wiki_summary_charts.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("[OK] Graphique 1 sauvegarde: charts/wiki_summary_charts.png")
    plt.close()


def create_period_analysis_chart():
    """Analyse par période historique"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Performance par Periode Historique - Momentum Optimal (10, 3M, Q)', 
                 fontsize=14, fontweight='bold')
    
    # === US ===
    ax1 = axes[0]
    periods_us = ['Complete', 'Pre-COVID', 'COVID\nRecovery', 'Bear\n2022', 'Bull\n2023-24']
    strat_us = [117.1, 6.1, 15.7, 0.0, 9.4]
    bench_us = [190.9, 37.5, 106.3, -9.1, 40.9]
    
    x = np.arange(len(periods_us))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, strat_us, width, label='Momentum Optimal', 
                    color='#3498db', edgecolor='black')
    bars2 = ax1.bar(x + width/2, bench_us, width, label='S&P 500', 
                    color='#e74c3c', edgecolor='black')
    
    ax1.set_ylabel('Rendement (%)', fontweight='bold')
    ax1.set_title('Etats-Unis (2018-2024)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(periods_us)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    ax1.axhline(y=0, color='black', linewidth=0.5)
    
    # === Europe ===
    ax2 = axes[1]
    periods_eu = ['Complete', 'Crise\nEuro', 'Recovery', 'Brexit', 'COVID\nCrise', '2022-24']
    strat_eu = [243.8, 15.4, 70.8, 0.8, -15.6, 39.9]
    bench_eu = [441.5, 22.5, 94.5, 40.9, -28.0, 32.6]
    
    x2 = np.arange(len(periods_eu))
    
    bars3 = ax2.bar(x2 - width/2, strat_eu, width, label='Momentum Optimal', 
                    color='#3498db', edgecolor='black')
    bars4 = ax2.bar(x2 + width/2, bench_eu, width, label='EURO STOXX', 
                    color='#e74c3c', edgecolor='black')
    
    ax2.set_ylabel('Rendement (%)', fontweight='bold')
    ax2.set_title('Europe (2010-2024)', fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(periods_eu)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=0, color='black', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('charts/wiki_period_analysis.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("[OK] Graphique 2 sauvegarde: charts/wiki_period_analysis.png")
    plt.close()


def create_grid_search_heatmap():
    """Heatmap des résultats du grid search Momentum"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Grid Search Momentum - Impact des Parametres (US 2018-2024)', 
                 fontsize=14, fontweight='bold')
    
    # Données simulées basées sur nos résultats
    lookbacks = [3, 6, 9, 12]
    n_stocks = [10, 20, 30]
    
    # Rendement moyen par paramètre (Mensuel)
    returns_monthly = np.array([
        [326.3, 170.6, 119.7, 143.8],  # N=10
        [207.1, 124.0, 113.3, 117.1],  # N=20
        [180.5, 117.5, 101.5, 121.0],  # N=30
    ])
    
    # Rendement moyen par paramètre (Trimestriel)
    returns_quarterly = np.array([
        [376.3, 253.4, 209.0, 213.3],  # N=10
        [210.3, 189.8, 198.5, 189.2],  # N=20
        [171.9, 206.0, 180.2, 188.3],  # N=30
    ])
    
    # Heatmap Mensuel
    ax1 = axes[0]
    im1 = ax1.imshow(returns_monthly, cmap='RdYlGn', aspect='auto', vmin=100, vmax=400)
    ax1.set_xticks(range(len(lookbacks)))
    ax1.set_yticks(range(len(n_stocks)))
    ax1.set_xticklabels([f'{l} mois' for l in lookbacks])
    ax1.set_yticklabels([f'{n} actions' for n in n_stocks])
    ax1.set_xlabel('Lookback (mois)', fontweight='bold')
    ax1.set_ylabel('Nombre d\'actions', fontweight='bold')
    ax1.set_title('Rebalancement Mensuel', fontweight='bold')
    
    # Ajouter les valeurs
    for i in range(len(n_stocks)):
        for j in range(len(lookbacks)):
            text = ax1.text(j, i, f'{returns_monthly[i, j]:.0f}%',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im1, ax=ax1, label='Rendement (%)')
    
    # Heatmap Trimestriel
    ax2 = axes[1]
    im2 = ax2.imshow(returns_quarterly, cmap='RdYlGn', aspect='auto', vmin=100, vmax=400)
    ax2.set_xticks(range(len(lookbacks)))
    ax2.set_yticks(range(len(n_stocks)))
    ax2.set_xticklabels([f'{l} mois' for l in lookbacks])
    ax2.set_yticklabels([f'{n} actions' for n in n_stocks])
    ax2.set_xlabel('Lookback (mois)', fontweight='bold')
    ax2.set_ylabel('Nombre d\'actions', fontweight='bold')
    ax2.set_title('Rebalancement Trimestriel', fontweight='bold')
    
    for i in range(len(n_stocks)):
        for j in range(len(lookbacks)):
            text = ax2.text(j, i, f'{returns_quarterly[i, j]:.0f}%',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im2, ax=ax2, label='Rendement (%)')
    
    plt.tight_layout()
    plt.savefig('charts/wiki_gridsearch_heatmap.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("[OK] Graphique 3 sauvegarde: charts/wiki_gridsearch_heatmap.png")
    plt.close()


def create_conclusion_chart():
    """Graphique de conclusion - Leçons apprises"""
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
    
    fig.suptitle('Lecons Apprises - Workshop Strategies Investissement', 
                 fontsize=16, fontweight='bold')
    
    # === 1. Pourcentage de réussite ===
    ax1 = fig.add_subplot(gs[0, 0])
    categories = ['US\n(Momentum)', 'Europe\n(Momentum)', 'Pros\nvs Indice']
    success_rates = [100, 25, 10]  # % de surperformance
    colors = ['#27ae60', '#e74c3c', '#f39c12']
    
    bars = ax1.bar(categories, success_rates, color=colors, edgecolor='black', linewidth=2)
    ax1.set_ylabel('% Surperformance', fontweight='bold')
    ax1.set_title('Taux de Réussite', fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, success_rates):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # === 2. Impact des frais ===
    ax2 = fig.add_subplot(gs[0, 1])
    fee_rates = [0, 0.5, 1.0]
    momentum_returns = [376.3, 267.3, 236.3]
    
    ax2.plot(fee_rates, momentum_returns, 'o-', linewidth=3, markersize=10, 
             color='#3498db', label='Momentum Optimal')
    ax2.axhline(y=190.9, color='red', linestyle='--', linewidth=2, label='S&P 500')
    ax2.set_xlabel('Frais de Transaction (%)', fontweight='bold')
    ax2.set_ylabel('Rendement (%)', fontweight='bold')
    ax2.set_title('Érosion par les Frais', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # === 3. Complexité vs Performance ===
    ax3 = fig.add_subplot(gs[1, :])
    strategies = ['ETF S&P 500\n(Buy & Hold)', 'Random + Stop-Loss', 
                  'Momentum (Base)', 'Momentum (Optimal)']
    complexity = [1, 3, 4, 5]
    performance = [190.9, 123.0, 117.1, 376.3]
    colors_scatter = ['#2ecc71', '#e74c3c', '#e74c3c', '#27ae60']
    
    scatter = ax3.scatter(complexity, performance, s=500, c=colors_scatter, 
                         edgecolors='black', linewidth=2, alpha=0.8)
    
    for i, txt in enumerate(strategies):
        ax3.annotate(txt, (complexity[i], performance[i]), 
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, fontweight='bold')
    
    ax3.axhline(y=190.9, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Benchmark')
    ax3.set_xlabel('Complexité de la Stratégie', fontweight='bold')
    ax3.set_ylabel('Rendement US 2018-2024 (%)', fontweight='bold')
    ax3.set_title('Complexité vs Performance', fontweight='bold')
    ax3.set_xticks([1, 2, 3, 4, 5])
    ax3.grid(alpha=0.3)
    ax3.legend()
    
    # === 4. Texte de conclusion ===
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    conclusion_text = """
    CONCLUSIONS CLES
    
    1. SUR LE MARCHE US : Le Momentum Optimal (10 actions, 3 mois, trimestriel) surperforme de +76% 
       avec des frais realistes (0.5%). C'est la seule strategie testee qui bat l'indice.
    
    2. SUR LE MARCHE EUROPEEN : Aucune strategie ne surperforme. Le Buy & Hold reste le meilleur choix.
    
    3. IMPACT DES FRAIS : Avec 1% de frais par transaction, l'avantage du Momentum fond a +45%, 
       mais reste positif. Au-dela, la strategie devient non rentable.
    
    4. COMPLEXITE : La strategie la plus simple (ETF) bat 90% des strategies actives sur le long terme.
       Plus on complexifie, plus on risque de sous-performer.
    
    5. RECOMMANDATION : Pour un investisseur lambda, un ETF World ou S&P 500 reste le meilleur choix.
       Le Momentum Optimal n'est viable que sur le marche US et avec des frais tres faibles.
    """
    
    ax4.text(0.05, 0.95, conclusion_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.savefig('charts/wiki_conclusion.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("[OK] Graphique 4 sauvegarde: charts/wiki_conclusion.png")
    plt.close()


def main():
    print("="*70)
    print("GÉNÉRATION DES GRAPHIQUES POUR LE WIKI GITHUB")
    print("="*70)
    
    # Créer le dossier charts s'il n'existe pas
    os.makedirs('charts', exist_ok=True)
    
    print("\n[1/4] Creation du graphique comparatif...")
    create_comparison_chart()
    
    print("\n[2/4] Creation de l'analyse par periode...")
    create_period_analysis_chart()
    
    print("\n[3/4] Creation des heatmaps...")
    create_grid_search_heatmap()
    
    print("\n[4/4] Creation du graphique de conclusion...")
    create_conclusion_chart()
    
    print("\n" + "="*70)
    print("TOUS LES GRAPHIQUES ONT ÉTÉ GÉNÉRÉS")
    print("="*70)
    print("\nFichiers créés:")
    print("  - charts/wiki_summary_charts.png")
    print("  - charts/wiki_period_analysis.png")
    print("  - charts/wiki_gridsearch_heatmap.png")
    print("  - charts/wiki_conclusion.png")


if __name__ == "__main__":
    main()
