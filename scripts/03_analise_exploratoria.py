import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


print("SCRIPT 3: ANÁLISE EXPLORATÓRIA DE DADOS DE DENGUE")


df = pd.read_csv('dengue_consolidado_2019_2025.csv', parse_dates=['DT_NOTIFIC', 'DT_SIN_PRI'])

df_confirmados = df[df['CLASSI_FIN'] == 10].copy()

df_confirmados['ANO'] = df_confirmados['DT_NOTIFIC'].dt.year
df_confirmados['MES'] = df_confirmados['DT_NOTIFIC'].dt.month
df_confirmados['DIA_SEMANA'] = df_confirmados['DT_NOTIFIC'].dt.dayofweek

print("\n CASOS CONFIRMADOS POR ANO:")
print(df_confirmados.groupby('ANO').size())

print("\n TOP 10 BAIRROS COM MAIS CASOS:")
top_bairros = df_confirmados['NM_BAIRRO'].value_counts().head(10)
print(top_bairros)

casos_por_mes = df_confirmados.groupby(['ANO', 'MES']).size().reset_index(name='CASOS')

plt.figure(figsize=(14, 6))
for ano in casos_por_mes['ANO'].unique():
    dados_ano = casos_por_mes[casos_por_mes['ANO'] == ano]
    plt.plot(dados_ano['MES'], dados_ano['CASOS'], marker='o', label=str(ano))

plt.title('Sazonalidade de Dengue em Recife (2019-2025)', fontsize=14)
plt.xlabel('Mês')
plt.ylabel('Número de Casos Confirmados')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sazonalidade_dengue.png', dpi=150)
print("\n Gráfico salvo: sazonalidade_dengue.png")

print("\n Estatísticas salvas com sucesso!")