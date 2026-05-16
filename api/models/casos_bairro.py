from sqlalchemy import Column, Integer, String
from api.database import Base

class CasoBairro(Base):
    __tablename__ = "casos_bairro"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    semana = Column(Integer, index=True)
    bairro = Column(String, index=True)
    casos = Column(Integer)