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
        
        # Calcular la desviación estándar y varianza
        desviacion_estandar = (suma_pesimista - suma_optimista) / 6
        varianza = desviacion_estandar ** 2
        
        return {
            "optimista": suma_optimista,
            "pesimista": suma_pesimista,
            "esperado": suma_esperado,
            "desviacion_estandar": desviacion_estandar,
            "varianza": varianza
        }

    def __str__(self):
        tareas_str = "\n".join(str(tarea) for tarea in self.tareas)
        tiempos = self.calcular_tiempos()
        return (f"Hito: {self.nombre}\n"
                f"  Suma Optimista: {tiempos['optimista']:.2f}\n"
                f"  Suma Pesimista: {tiempos['pesimista']:.2f}\n"
                f"  Desviación Estándar: {tiempos['desviacion_estandar']:.2f}\n"
                f"  Varianza: {tiempos['varianza']:.2f}\n"
                f"{tareas_str}")
