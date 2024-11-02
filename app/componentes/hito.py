from .componente_proyecto import ComponenteProyecto

class Hito(ComponenteProyecto):
    def __init__(self, nombre):
        self.nombre = nombre
        self.tareas = []

    def agregar(self, tarea):
        self.tareas.append(tarea)

    def calcular_tiempos(self):
        suma_optimista = sum(tarea.calcular_tiempos()["optimista"] for tarea in self.tareas)
        suma_pesimista = sum(tarea.calcular_tiempos()["pesimista"] for tarea in self.tareas)
        suma_esperado = sum(tarea.calcular_tiempos()["esperado"] for tarea in self.tareas)
        return {"optimista": suma_optimista, "pesimista": suma_pesimista, "esperado": suma_esperado}
    
    def __str__(self):
        tareas_str = "\n".join(str(tarea) for tarea in self.tareas)
        return f"Hito: {self.nombre}\n{tareas_str}"
