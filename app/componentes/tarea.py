from .componente_proyecto import ComponenteProyecto


class Tarea(ComponenteProyecto):
    def __init__(self, nombre):
        self.nombre = nombre
        self.subtareas = []

    def agregar(self, subtarea):
        self.subtareas.append(subtarea)

    def calcular_tiempos(self):
        suma_optimista = sum(subtarea.calcular_tiempos()["optimista"] for subtarea in self.subtareas)
        suma_pesimista = sum(subtarea.calcular_tiempos()["pesimista"] for subtarea in self.subtareas)
        suma_esperado = sum(subtarea.calcular_tiempos()["esperado"] for subtarea in self.subtareas)
        return {"optimista": suma_optimista, "pesimista": suma_pesimista, "esperado": suma_esperado}
    
    def __str__(self):
        subtareas_str = "\n".join(str(subtarea) for subtarea in self.subtareas)
        return f"  Tarea: {self.nombre}\n{subtareas_str}"
