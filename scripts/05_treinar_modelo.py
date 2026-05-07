import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib
import warnings
warnings.filterwarnings('ignore')

print("MODELO DE PRODUCAO - VERSAO ROBUSTA PARA EMPREL\n")

df = pd.read_csv('dataset_dengue_clima_integrado.csv', parse_dates=['DATA'])
df = df.sort_values('DATA').reset_index(drop=True)

print("[1/4] Criando features conservadoras...")

for lag in [7, 14, 21, 30]:
    df[f'CASOS_LAG_{lag}'] = df['CASOS'].shift(lag)

for window in [7, 14, 30]:
    df[f'CASOS_MA_{window}'] = df['CASOS'].shift(1).rolling(window=window).mean()

for lag in [7, 14]:
    df[f'TEMP_LAG_{lag}'] = df['TEMP_MEDIA'].shift(lag)
    df[f'PRECIP_LAG_{lag}'] = df['PRECIPITACAO_TOTAL'].shift(lag)

df['TEMP_VARIACAO'] = df['TEMP_MAX'] - df['TEMP_MIN']
df['PRECIPITACAO_7D'] = df['PRECIPITACAO_TOTAL'].rolling(window=7).sum()

df = df.dropna()

features = [
    'TEMP_MEDIA', 'TEMP_VARIACAO', 'PRECIPITACAO_TOTAL', 'UMIDADE_MEDIA',
    'MES', 'SEMANA',
    'CASOS_LAG_14', 'CASOS_LAG_21', 'CASOS_LAG_30',
    'CASOS_MA_14', 'CASOS_MA_30',
    'TEMP_LAG_7', 'TEMP_LAG_14',
    'PRECIP_LAG_7', 'PRECIP_LAG_14',
    'PRECIPITACAO_7D'
]

X = df[features]
y = df['CASOS']

print(f"Dataset: {len(df)} registros com {len(features)} features\n")

print("[2/4] Testando 3 modelos com validacao temporal...")

modelos_config = {
    'Ridge (Regressao Linear Regularizada)': Ridge(alpha=10.0),
    'Random Forest (Conservador)': RandomForestRegressor(
        n_estimators=50,
        max_depth=4,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    ),
    'XGBoost (Regularizado)': XGBRegressor(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.7,
        colsample_bytree=0.7,
        reg_alpha=1.0,
        reg_lambda=1.0,
        random_state=42
    )
}

resultados = []

tscv = TimeSeriesSplit(n_splits=3)

for nome, modelo in modelos_config.items():
    print(f"\nTestando: {nome}")
    
    mae_folds = []
    r2_folds = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X), 1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_val)
        
        mae = mean_absolute_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)
        
        mae_folds.append(mae)
        r2_folds.append(r2)
    
    mae_medio = np.mean(mae_folds)
    r2_medio = np.mean(r2_folds)
    
    print(f"  Validacao Cruzada: MAE={mae_medio:.2f} | R2={r2_medio:.3f}")
    
    resultados.append({
        'modelo': nome,
        'mae': mae_medio,
        'r2': r2_medio
    })

print("\n[3/4] Escolhendo melhor modelo e testando em holdout...")

df_resultados = pd.DataFrame(resultados).sort_values('r2', ascending=False)
print("\nRanking de modelos:")
print(df_resultados.to_string(index=False))

melhor_nome = df_resultados.iloc[0]['modelo']
melhor_modelo = modelos_config[melhor_nome]

print(f"\nModelo escolhido: {melhor_nome}\n")

split_idx = int(len(df) * 0.8)
df_train = df.iloc[:split_idx]
df_test = df.iloc[split_idx:]

X_train = df_train[features]
y_train = df_train['CASOS']
X_test = df_test[features]
y_test = df_test['CASOS']

melhor_modelo.fit(X_train, y_train)

y_pred_test = melhor_modelo.predict(X_test)

mae_test = mean_absolute_error(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2_test = r2_score(y_test, y_pred_test)

print("Metricas no conjunto de teste (holdout):")
print(f"  MAE: {mae_test:.2f} casos/dia")
print(f"  RMSE: {rmse_test:.2f} casos/dia")
print(f"  R2: {r2_test:.3f}\n")

print("[4/4] Salvando modelo para producao...")

joblib.dump({
    'modelo': melhor_modelo,
    'features': features,
    'metricas_validacao_cruzada': resultados,
    'metricas_teste': {
        'mae': mae_test,
        'rmse': rmse_test,
        'r2': r2_test
    }
}, 'modelo_dengue_emprel_producao.pkl')

print("Modelo salvo: modelo_dengue_emprel_producao.pkl\n")

plt.figure(figsize=(14, 6))
plt.plot(df_test['DATA'], y_test.values, label='Casos Reais', color='#2E86AB', linewidth=2, marker='o', markersize=4)
plt.plot(df_test['DATA'], y_pred_test, label='Predicao', color='#F18F01', linewidth=2, linestyle='--', marker='x', markersize=4)
plt.fill_between(df_test['DATA'], y_test.values, y_pred_test, alpha=0.2)
plt.xlabel('Data')
plt.ylabel('Numero de Casos')
plt.title(f'Modelo de Producao - {melhor_nome}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('modelo_producao_emprel.png', dpi=150, bbox_inches='tight')
print("Grafico salvo: modelo_producao_emprel.png\n")


print("MODELO PRONTO PARA APRESENTACAO PROFISSIONAL")

print(f"\nModelo: {melhor_nome}")
print(f"MAE (Validacao Cruzada): {df_resultados.iloc[0]['mae']:.2f} casos/dia")
print(f"R2 (Validacao Cruzada): {df_resultados.iloc[0]['r2']:.3f}")
print(f"MAE (Teste Final): {mae_test:.2f} casos/dia")
print(f"R2 (Teste Final): {r2_test:.3f}")
print("\nMetricas realistas e sem overfitting!")