# app/models/subtarea_db.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SubtareaDB(Base):
    __tablename__ = "subtareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    tiempo_probable = Column(Float, nullable=False, default=0.0)
    tiempo_optimista = Column(Float, nullable=False, default=0.0)
    tiempo_pesimista = Column(Float, nullable=False, default=0.0)
    tiempo_esperado = Column(Float, nullable=False, default=0.0)
    tarea_id = Column(Integer, ForeignKey("tareas.id"))
    dependencia_id = Column(Integer, ForeignKey("subtareas.id"), nullable=True)  # Dependencia con otra subtarea

    tarea = relationship("TareaDB", back_populates="subtareas")
    dependencia = relationship("SubtareaDB", remote_side=[id], backref="dependientes")
