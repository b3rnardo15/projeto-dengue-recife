from fastapi import APIRouter, HTTPException, Query
from api.database import get_database
from typing import Optional

router = APIRouter()

@router.get("/historico")
async def obter_historico(
    ano: Optional[int] = Query(None, description="Filtrar por ano"),
    semana: Optional[int] = Query(None, description="Filtrar por semana"),
    limite: int = Query(100, ge=1, le=500, description="Número máximo de registros")
):
    try:
        db = get_database()
        filtro = {}
        
        if ano:
            filtro["ANO"] = ano
        if semana:
            filtro["SEMANA"] = semana
        
        historico = list(
            db.casos_dengue.find(filtro, {"_id": 0})
            .sort([("ANO", -1), ("SEMANA", -1)])
            .limit(limite)
        )
        
        return historico
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

@router.get("/predicoes")
async def listar_predicoes(limite: int = Query(10, ge=1, le=100)):
    try:
        db = get_database()
        predicoes = list(
            db.predicoes.find({}, {"_id": 0})
            .sort("data_predicao", -1)
            .limit(limite)
        )
        return predicoes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar predições: {str(e)}")