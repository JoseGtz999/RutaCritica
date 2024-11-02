from .componente_proyecto import ComponenteProyecto


class Subtarea(ComponenteProyecto):
    def __init__(self, nombre, tiempo_probable):
        self.nombre = nombre
        self.tiempo_probable = tiempo_probable
        self.tiempo_optimista = self.calcular_optimista()
        self.tiempo_pesimista = self.calcular_pesimista()
        self.tiempo_esperado = self.calcular_esperado()

    def calcular_optimista(self):
        return self.tiempo_probable - 1

    def calcular_pesimista(self):
        return self.tiempo_probable + 2

    def calcular_esperado(self):
        return (self.tiempo_optimista + self.tiempo_probable * 4 + self.tiempo_pesimista) / 6

    def calcular_tiempos(self):
        return {"optimista": self.tiempo_optimista, "pesimista": self.tiempo_pesimista, "esperado": self.tiempo_esperado}
    
    def __str__(self):
        return (f"    Subtarea: {self.nombre}\n"
                f"      - Tiempo Probable: {self.tiempo_probable}\n"
                f"      - Tiempo Optimista: {self.tiempo_optimista:.2f}\n"
                f"      - Tiempo Pesimista: {self.tiempo_pesimista:.2f}\n"
                f"      - Tiempo Esperado: {self.tiempo_esperado:.2f}")
