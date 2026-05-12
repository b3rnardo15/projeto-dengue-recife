from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DadosClimaInput(BaseModel):
    precipitacao_mm: float = Field(..., description="Precipitação total em mm")
    temp_media_c: float = Field(..., description="Temperatura média em °C")
    umidade_media: float = Field(..., description="Umidade relativa média em %")
    ano: int = Field(..., description="Ano da predição")
    semana: int = Field(..., ge=1, le=53, description="Semana do ano (1-53)")

class PredicaoOutput(BaseModel):
    casos_preditos: float = Field(..., description="Número de casos preditos")
    ano: int
    semana: int
    data_predicao: datetime = Field(default_factory=datetime.now)
    
class HistoricoResponse(BaseModel):
    ano: int
    semana: int
    casos: int
    precipitacao_mm: Optional[float] = None
    temp_media_c: Optional[float] = None
    umidade_media: Optional[float] = None