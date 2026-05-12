import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

print("ANALISE EXPLORATORIA - DENGUE")


df = pd.read_csv('data/processed/dengue_consolidado_2019_2025.csv')

print(f"\nTotal de semanas: {len(df)}")
print(f"Total de casos: {df['CASOS'].sum()}")
print(f"\nEstatisticas:")
print(df['CASOS'].describe())

output_path = Path('reports/figures')
output_path.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Gráfico 1: Casos por semana
plt.figure(figsize=(14, 6))
plt.plot(range(len(df)), df['CASOS'], linewidth=1.5, color='crimson')
plt.title('Casos de Dengue por Semana - Recife (2021-2025)', fontsize=14, fontweight='bold')
plt.xlabel('Semana', fontsize=12)
plt.ylabel('Número de Casos', fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output_path / 'casos_por_semana.png', dpi=300, bbox_inches='tight')
print("\nGrafico salvo: casos_por_semana.png")
plt.close()

# Gráfico 2: Casos por ano
casos_ano = df.groupby('ANO')['CASOS'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(casos_ano['ANO'], casos_ano['CASOS'], color='steelblue', edgecolor='black')
plt.title('Total de Casos por Ano - Recife', fontsize=14, fontweight='bold')
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Total de Casos', fontsize=12)
plt.xticks(casos_ano['ANO'])
for i, v in enumerate(casos_ano['CASOS']):
    plt.text(casos_ano['ANO'].iloc[i], v + 200, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(output_path / 'casos_por_ano.png', dpi=300, bbox_inches='tight')
print("Grafico salvo: casos_por_ano.png")
plt.close()

# Gráfico 3: Média de casos por semana do ano
media_semana = df.groupby('SEMANA')['CASOS'].mean().reset_index()
plt.figure(figsize=(14, 6))
plt.plot(media_semana['SEMANA'], media_semana['CASOS'], marker='o', linewidth=2, markersize=4, color='darkgreen')
plt.title('Média de Casos por Semana do Ano (Sazonalidade)', fontsize=14, fontweight='bold')
plt.xlabel('Semana do Ano', fontsize=12)
plt.ylabel('Média de Casos', fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(output_path / 'sazonalidade.png', dpi=300, bbox_inches='tight')
print("Grafico salvo: sazonalidade.png")
plt.close()

print("\nAnalise concluida!")