# app/models/proyecto_db.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProyectoDB(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    descripcion = Column(String, default="")

    hitos = relationship("HitoDB", back_populates="proyecto", cascade="all, delete-orphan")

    # Campos adicionales para tiempos calculados (esto puede ser opcional si no se necesita persistir en la base de datos)
    tiempo_optimista_total = Column(Float, nullable=True)
    tiempo_pesimista_total = Column(Float, nullable=True)
    tiempo_esperado_total = Column(Float, nullable=True)
    desviacion_estandar_total = Column(Float, nullable=True)

