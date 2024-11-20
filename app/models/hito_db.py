# app/models/hito_db.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class HitoDB(Base):
    __tablename__ = "hitos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    tiempo_optimista = Column(Float, nullable=True)
    tiempo_pesimista = Column(Float, nullable=True)
    tiempo_esperado = Column(Float, nullable=True)
    varianza = Column(Float, nullable=True)
    desviacion_estandar = Column(Float, nullable=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))

    proyecto = relationship("ProyectoDB", back_populates="hitos")
    tareas = relationship("TareaDB", back_populates="hito", cascade="all, delete-orphan")

