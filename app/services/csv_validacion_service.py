import csv
from typing import List, Dict, Any
from io import StringIO

class CSVValidacionService:
    def __init__(self, file):
        self.file = file  # El archivo se pasa como un objeto StringIO
        self.required_columns = ["hito", "tarea", "subtarea", "dependencia", "tiempo esperado"]

    def cargar_csv(self) -> List[Dict[str, Any]]:
        """
        Carga el archivo CSV desde el archivo en memoria y devuelve las filas como un diccionario.
        """
        self.file.seek(0)  # Asegúrate de que el archivo está al principio
        reader = csv.DictReader(self.file)
        return list(reader)

    def validar_estructura(self, filas: List[Dict[str, Any]]) -> List[str]:
        """
        Valida que todas las filas contengan las columnas requeridas.
        """
        errores = []
        
        # Verificar que todas las columnas requeridas estén presentes
        missing_columns = [col for col in self.required_columns if col not in filas[0]]
        if missing_columns:
            errores.append(f"Faltan las siguientes columnas en el archivo CSV: {', '.join(missing_columns)}")
        
        # Verificar que todas las filas tengan las columnas requeridas
        for idx, fila in enumerate(filas, 1):
            for col in self.required_columns:
                if col not in fila or (not fila[col] and col != "dependencia"):  # Permitir dependencias vacías
                    errores.append(f"En la fila {idx}, falta el valor de la columna '{col}'.")
        
        return errores

    def validar_contenido(self, filas: List[Dict[str, Any]]) -> List[str]:
        """
        Valida que los datos de cada columna sean correctos.
        """
        errores = []

        for idx, fila in enumerate(filas, 1):
            # Validar tiempos como valores numéricos
            for campo in ["tiempo esperado"]:
                try:
                    valor = float(fila[campo])
                    if valor < 0:
                        errores.append(f"En la fila {idx}, el valor de '{campo}' no puede ser negativo.")
                except ValueError:
                    errores.append(f"En la fila {idx}, el valor de '{campo}' no es un número válido.")

            # Validar dependencias, permitiendo valores vacíos y múltiples valores separados por comas
            if fila["dependencia"]:  # Solo valida si hay un valor en la columna
                dependencias = fila["dependencia"].split(",")
                for dep in dependencias:
                    dep = dep.strip()  # Elimina espacios en blanco
                    # Validar el formato X.X.X... para las dependencias
                    if not dep.replace(".", "").isdigit():
                        errores.append(f"En la fila {idx}, el campo 'dependencia' contiene un valor no numérico o mal formado: '{dep}'.")
        
        return errores

    def validar(self) -> List[str]:
        """
        Valida el archivo CSV en cuanto a estructura y contenido.
        """
        try:
            filas = self.cargar_csv()
        except FileNotFoundError as e:
            return [str(e)]
        
        errores_estructura = self.validar_estructura(filas)
        errores_contenido = self.validar_contenido(filas)

        return errores_estructura + errores_contenido

    def procesar(self) -> Dict[str, Any]:
        """
        Ejecuta la validación y devuelve los resultados.
        """
        errores = self.validar()
        if errores:
            return {"estado": "error", "errores": errores}
        return {"estado": "exito", "mensaje": "Archivo CSV validado correctamente."}


