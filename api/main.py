from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import predict, historico

app = FastAPI(
    title="API de Predição de Dengue - Recife",
    description="Sistema de predição de casos de dengue baseado em dados climáticos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/v1", tags=["Predições"])
app.include_router(historico.router, prefix="/api/v1", tags=["Histórico"])

@app.get("/")
async def root():
    return {
        "message": "API de Predição de Dengue - Recife",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}