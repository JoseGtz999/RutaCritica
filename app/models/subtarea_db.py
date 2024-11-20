# app/models/subtarea_db.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY  # Importar ARRAY para PostgreSQL
from app.database import Base

class SubtareaDB(Base):
    __tablename__ = "subtareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    PERT = Column(Float, nullable=False, default=0.0)
    tiempo_optimista = Column(Float, nullable=False, default=0.0)
    tiempo_pesimista = Column(Float, nullable=False, default=0.0)
    tiempo_probable = Column(Float, nullable=False, default=0.0)
    tarea_id = Column(Integer, ForeignKey("tareas.id"))
    dependencia_id = Column(ARRAY(String), nullable=True, default=list)  # Usar ARRAY para listas de enteros
    subtarea_id_csv = Column(String, nullable=True, default="0") # Cambiar a String para almacenar '1.1.1'

    tarea = relationship("TareaDB", back_populates="subtareas")
