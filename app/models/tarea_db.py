# app/models/tarea_db.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TareaDB(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    hito_id = Column(Integer, ForeignKey("hitos.id"))

    hito = relationship("HitoDB", back_populates="tareas")
    subtareas = relationship("SubtareaDB", back_populates="tarea", cascade="all, delete-orphan")
