# app/models/subtarea.py
from pydantic import BaseModel, Field

class Subtarea(BaseModel):
    nombre: str
    tiempo_probable: float = Field(..., gt=0)

    def calcular_optimista(self) -> float:
        return self.tiempo_probable - 1

    def calcular_pesimista(self) -> float:
        return self.tiempo_probable + 2

    def calcular_esperado(self) -> float:
        return (self.calcular_optimista() + 4 * self.tiempo_probable + self.calcular_pesimista()) / 6

    def calcular_tiempos(self) -> dict:
        return {
            "optimista": self.calcular_optimista(),
            "pesimista": self.calcular_pesimista(),
            "esperado": self.calcular_esperado()
        }

    def __str__(self):
        return (f"    Subtarea: {self.nombre}\n"
                f"      - Tiempo Probable: {self.tiempo_probable}\n"
                f"      - Tiempo Optimista: {self.calcular_optimista():.2f}\n"
                f"      - Tiempo Pesimista: {self.calcular_pesimista():.2f}\n"
                f"      - Tiempo Esperado: {self.calcular_esperado():.2f}")
