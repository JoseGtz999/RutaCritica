from componentes.hito import Hito
from componentes.tarea import Tarea
from componentes.subtarea import Subtarea
from calculos.calculos_totales import CalculosTotales

def ingresar_proyecto():
    hitos = []

    num_hitos = int(input("Ingrese el número de hitos en el proyecto: "))
    for i in range(num_hitos):
        nombre_hito = input(f"\nIngrese el nombre del hito {i + 1}: ")
        hito = Hito(nombre_hito)

        num_tareas = int(input(f"Ingrese el número de tareas para el hito '{nombre_hito}': "))
        for j in range(num_tareas):
            nombre_tarea = input(f"  Ingrese el nombre de la tarea {j + 1} para el hito '{nombre_hito}': ")
            tarea = Tarea(nombre_tarea)

            num_subtareas = int(input(f"    Ingrese el número de subtareas para la tarea '{nombre_tarea}': "))
            for k in range(num_subtareas):
                nombre_subtarea = input(f"      Ingrese el nombre de la subtarea {k + 1} para la tarea '{nombre_tarea}': ")
                tiempo_probable = float(input(f"        Ingrese el tiempo más probable para la subtarea '{nombre_subtarea}': "))

                subtarea = Subtarea(nombre_subtarea, tiempo_probable)
                tarea.agregar(subtarea)

            hito.agregar(tarea)

        hitos.append(hito)

    return hitos

def mostrar_resumen(hitos):
    print("\nResumen del proyecto:")
    for hito in hitos:
        print(hito)

    calculos_totales = CalculosTotales(hitos).calcular_totales()
    print("\nCálculos Totales del Proyecto:")
    for key, value in calculos_totales.items():
        print(f"{key}: {value:.2f}")

if __name__ == "__main__":
    hitos = ingresar_proyecto()
    mostrar_resumen(hitos)
