from abc import ABC, abstractmethod

class ComponenteProyecto(ABC):
    @abstractmethod
    def calcular_tiempos(self):
        pass

    def agregar(self, componente):
        pass  # Solo aplicable a `Tarea` y `Hito`
