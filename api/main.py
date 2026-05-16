# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_database

app = FastAPI(
    title="API de Predicao de Dengue - Recife",
    description="Sistema de predicao de casos de dengue baseado em dados climaticos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "API de Predicao de Dengue - Recife",
        "status": "online",
        "versao": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "casos": "/api/casos",
            "bairros": "/api/bairros",
            "ranking": "/api/bairros/ranking",
            "resumo": "/api/estatisticas/resumo"
        }
    }

@app.get("/health")
async def health_check():
    try:
        db = get_database()
        count_dengue = db.casos_dengue.count_documents({})
        count_bairros = db.casos_por_bairro.count_documents({})
        return {
            "status": "healthy",
            "database": "connected",
            "casos_dengue": count_dengue,
            "casos_bairros": count_bairros
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/api/casos")
async def get_casos(ano: int = None, semana: int = None):
    db = get_database()
    filtro = {}
    if ano:
        filtro["ANO"] = ano
    if semana:
        filtro["SEMANA"] = semana
    
    casos = list(db.casos_dengue.find(filtro, {"_id": 0}).sort([("ANO", 1), ("SEMANA", 1)]))
    
    for caso in casos:
        for key, value in caso.items():
            if isinstance(value, float):
                if value != value:
                    caso[key] = None
    
    return {"total": len(casos), "dados": casos}

@app.get("/api/bairros")
async def get_bairros():
    db = get_database()
    bairros = db.casos_por_bairro.distinct("BAIRRO")
    return {"total": len(bairros), "bairros": sorted(bairros)}

@app.get("/api/casos/bairros")
async def get_casos_bairro(bairro: str = None, ano: int = None):
    db = get_database()
    filtro = {}
    if bairro:
        filtro["BAIRRO"] = bairro
    if ano:
        filtro["ANO"] = ano
    
    casos = list(db.casos_por_bairro.find(filtro, {"_id": 0}).sort([("ANO", 1), ("SEMANA", 1)]))
    return {"total": len(casos), "dados": casos}

@app.get("/api/bairros/ranking")
async def get_ranking_bairros(ano: int = None, limit: int = 10):
    db = get_database()
    match_stage = {"ANO": ano} if ano else {}
    
    pipeline = [
        {"$match": match_stage},
        {"$group": {"_id": "$BAIRRO", "total_casos": {"$sum": "$CASOS"}}},
        {"$sort": {"total_casos": -1}},
        {"$limit": limit}
    ]
    
    resultado = list(db.casos_por_bairro.aggregate(pipeline))
    return {
        "ranking": [
            {"bairro": r["_id"], "casos": r["total_casos"]} 
            for r in resultado
        ]
    }

@app.get("/api/bairros/todos")
async def get_todos_bairros_com_casos(ano: int = None):
    db = get_database()
    match_stage = {"ANO": ano} if ano else {}
    
    pipeline = [
        {"$match": match_stage},
        {"$group": {"_id": "$BAIRRO", "total_casos": {"$sum": "$CASOS"}}},
        {"$sort": {"total_casos": -1}}
    ]
    
    resultado = list(db.casos_por_bairro.aggregate(pipeline))
    
    bairros_limpos = []
    for r in resultado:
        bairro = r["_id"]
        casos = r["total_casos"]
        
        if bairro is None or bairro == "":
            continue
        
        if isinstance(casos, float):
            if casos != casos:
                casos = 0
        
        bairros_limpos.append({
            "bairro": str(bairro), 
            "casos": int(casos) if casos else 0
        })
    
    return {
        "total_bairros": len(bairros_limpos),
        "periodo": f"Ano {ano}" if ano else "2020-2025",
        "bairros": bairros_limpos
    }
@app.get("/api/casos/bairros/por-ano")
async def get_casos_bairros_por_ano(ano: int):
    db = get_database()
    
    pipeline = [
        {"$match": {"ANO": ano}},
        {"$group": {
            "_id": "$BAIRRO",
            "total_casos": {"$sum": "$CASOS"},
            "total_semanas": {"$sum": 1}
        }},
        {"$sort": {"total_casos": -1}}
    ]
    
    resultado = list(db.casos_por_bairro.aggregate(pipeline))
    
    bairros_ano = []
    for r in resultado:
        bairro = r["_id"]
        if bairro is None or bairro == "":
            continue
        
        bairros_ano.append({
            "bairro": str(bairro),
            "casos": int(r["total_casos"]),
            "semanas_com_casos": int(r["total_semanas"])
        })
    
    total_casos_ano = sum(b["casos"] for b in bairros_ano)
    
    return {
        "ano": ano,
        "total_casos": total_casos_ano,
        "total_bairros": len(bairros_ano),
        "bairros": bairros_ano
    }


@app.get("/api/bairros")
async def get_lista_bairros():
    db = get_database()
    bairros = sorted(db.casos_por_bairro.distinct("BAIRRO"))
    
    bairros_limpos = [b for b in bairros if b and b != ""]
    
    return {
        "total": len(bairros_limpos),
        "bairros": bairros_limpos
    }

@app.get("/api/bairros/{bairro}/timeline")
async def get_timeline_bairro(bairro: str):
    db = get_database()
    
    casos = list(db.casos_por_bairro.find(
        {"BAIRRO": bairro},
        {"_id": 0}
    ).sort([("ANO", 1), ("SEMANA", 1)]))
    
    total = sum(c["CASOS"] for c in casos)
    
    return {
        "bairro": bairro,
        "total_casos": total,
        "total_semanas": len(casos),
        "timeline": casos
    }

@app.get("/api/estatisticas/resumo")
async def get_estatisticas_resumo():
    db = get_database()
    
    pipeline_total = [
        {"$group": {"_id": None, "total": {"$sum": "$CASOS"}}}
    ]
    total_casos = list(db.casos_por_bairro.aggregate(pipeline_total))
    
    total_bairros = len(db.casos_por_bairro.distinct("BAIRRO"))
    anos = sorted(db.casos_por_bairro.distinct("ANO"))
    
    pipeline_ano = [
        {"$group": {"_id": "$ANO", "total": {"$sum": "$CASOS"}}},
        {"$sort": {"_id": 1}}
    ]
    casos_por_ano = list(db.casos_por_bairro.aggregate(pipeline_ano))
    
    return {
        "total_casos": total_casos[0]["total"] if total_casos else 0,
        "total_bairros": total_bairros,
        "periodo": f"{anos[0]}-{anos[-1]}" if anos else "N/A",
        "casos_por_ano": [
            {"ano": c["_id"], "casos": c["total"]} 
            for c in casos_por_ano
        ]
    }