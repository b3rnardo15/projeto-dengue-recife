from fastapi import APIRouter, HTTPException, Query
from api.models import HistoricoResponse
from api.database import get_database
from typing import List, Optional

router = APIRouter()

@router.get("/historico", response_model=List[HistoricoResponse])
async def obter_historico(
    ano: Optional[int] = Query(None, description="Filtrar por ano"),
    limite: int = Query(100, ge=1, le=500, description="Número máximo de registros")
):
    try:
        db = get_database()
        
        filtro = {}
        if ano:
            filtro["ano"] = ano
        
        resultados = list(
            db.casos_dengue.find(filtro, {"_id": 0})
            .sort([("ano", -1), ("semana", -1)])
            .limit(limite)
        )
        
        return resultados
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

@router.get("/predicoes", response_model=List[dict])
async def obter_predicoes(limite: int = Query(50, ge=1, le=200)):
    try:
        db = get_database()
        predicoes = list(
            db.predicoes.find({}, {"_id": 0})
            .sort("data_predicao", -1)
            .limit(limite)
        )
        return predicoes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar predições: {str(e)}")