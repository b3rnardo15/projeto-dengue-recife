from fastapi import APIRouter, HTTPException
from api.models import DadosClimaInput, PredicaoOutput
from api.database import get_database
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

router = APIRouter()

MODEL_PATH = Path("models/modelo_dengue_emprel_producao.pkl")
modelo_dict = None

def carregar_modelo():
    global modelo_dict
    if modelo_dict is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}")
        modelo_dict = joblib.load(MODEL_PATH)
    return modelo_dict

@router.post("/predict", response_model=PredicaoOutput)
async def fazer_predicao(dados: DadosClimaInput):
    try:
        modelo_data = carregar_modelo()
        modelo = modelo_data['modelo']
        features = modelo_data['features']
        
        # Criar DataFrame com valores padrão para features não fornecidas
        df_input = pd.DataFrame([{
            'TEMP_MEDIA': dados.temp_media_c,
            'TEMP_VARIACAO': 0.0,  # Padrão
            'PRECIPITACAO_TOTAL': dados.precipitacao_mm,
            'UMIDADE_MEDIA': dados.umidade_media,
            'MES': (dados.semana // 4) + 1,  # Estimativa
            'SEMANA': dados.semana,
            'CASOS_LAG_14': 100.0,  # Valor médio padrão
            'CASOS_LAG_21': 100.0,
            'CASOS_LAG_30': 100.0,
            'CASOS_MA_14': 100.0,
            'CASOS_MA_30': 100.0,
            'TEMP_LAG_7': dados.temp_media_c,
            'TEMP_LAG_14': dados.temp_media_c,
            'PRECIP_LAG_7': dados.precipitacao_mm,
            'PRECIP_LAG_14': dados.precipitacao_mm,
            'PRECIPITACAO_7D': dados.precipitacao_mm
        }])
        
        # Garantir ordem das features
        df_input = df_input[features]
        
        predicao = modelo.predict(df_input)[0]
        predicao = max(0, round(predicao, 2))
        
        db = get_database()
        db.predicoes.insert_one({
            "ano": dados.ano,
            "semana": dados.semana,
            "casos_preditos": predicao,
            "precipitacao_mm": dados.precipitacao_mm,
            "temp_media_c": dados.temp_media_c,
            "umidade_media": dados.umidade_media,
            "data_predicao": datetime.now()
        })
        
        return PredicaoOutput(
            casos_preditos=predicao,
            ano=dados.ano,
            semana=dados.semana
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")