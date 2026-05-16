# api/routes/bairros.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from api.database import get_database

router = APIRouter(prefix="/bairros", tags=["Bairros"])

@router.get("/casos")
async def get_casos_por_bairro(
    bairro: Optional[str] = None,
    ano: Optional[int] = None,
    semana: Optional[int] = None
):
    db = get_database()
    collection = db['casos_por_bairro']
    
    filtro = {}
    if bairro:
        filtro['BAIRRO'] = bairro
    if ano:
        filtro['ANO'] = ano
    if semana:
        filtro['SEMANA'] = semana
    
    dados = list(collection.find(filtro, {'_id': 0}).sort([('ANO', 1), ('SEMANA', 1)]))
    
    return {
        "total": len(dados),
        "filtros": filtro,
        "dados": dados
    }

@router.get("/ranking")
async def get_ranking_bairros(ano: Optional[int] = None, limite: int = Query(10, le=50)):
    db = get_database()
    collection = db['casos_por_bairro']
    
    match_stage = {"$match": {"ANO": ano}} if ano else {"$match": {}}
    
    pipeline = [
        match_stage,
        {"$group": {"_id": "$BAIRRO", "total_casos": {"$sum": "$CASOS"}}},
        {"$sort": {"total_casos": -1}},
        {"$limit": limite}
    ]
    
    ranking = list(collection.aggregate(pipeline))
    
    return {
        "ano": ano or "todos",
        "total_bairros": len(ranking),
        "ranking": [{"bairro": r["_id"], "casos": r["total_casos"]} for r in ranking]
    }

@router.get("/lista")
async def listar_bairros():
    db = get_database()
    collection = db['casos_por_bairro']
    
    bairros = collection.distinct("BAIRRO")
    
    return {
        "total": len(bairros),
        "bairros": sorted(bairros)
    }