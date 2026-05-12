import requests
import pandas as pd
from typing import List, Dict

API_BASE_URL = "http://localhost:8000/api/v1"

def carregar_historico(ano: int = None, limite: int = 200) -> pd.DataFrame:
    """Carrega dados históricos da API"""
    try:
        params = {"limite": limite}
        if ano:
            params["ano"] = ano
        
        response = requests.get(f"{API_BASE_URL}/historico", params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return pd.DataFrame()

def carregar_predicoes(limite: int = 50) -> pd.DataFrame:
    """Carrega predições da API"""
    try:
        response = requests.get(f"{API_BASE_URL}/predicoes", params={"limite": limite})
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        if 'data_predicao' in df.columns:
            df['data_predicao'] = pd.to_datetime(df['data_predicao'])
        
        return df
    except Exception as e:
        print(f"Erro ao carregar predições: {e}")
        return pd.DataFrame()

def fazer_predicao(precipitacao: float, temperatura: float, umidade: float, 
                   ano: int, semana: int) -> Dict:
    """Faz uma nova predição via API"""
    try:
        payload = {
            "precipitacao_mm": precipitacao,
            "temp_media_c": temperatura,
            "umidade_media": umidade,
            "ano": ano,
            "semana": semana
        }
        
        response = requests.post(f"{API_BASE_URL}/predict", json=payload)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"Erro ao fazer predição: {e}")
        return None