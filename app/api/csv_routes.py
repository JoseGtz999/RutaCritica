from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db  # Asegúrate de que get_db esté importado
from app.services.csv_validacion_service import CSVValidacionService  # Importa correctamente la clase
from app.services.proyecto_service import insertar_datos_proyecto
from io import StringIO
import csv

router = APIRouter()

@router.post("/rutaCritica/validar_proyecto")
async def validar_proyecto_desde_csv(file: UploadFile, db: AsyncSession = Depends(get_db)):
    try:
        # Leer y validar el archivo CSV
        csv_content = await file.read()
        csv_file = StringIO(csv_content.decode("utf-8"))
        
        # Inicializar el servicio de validación de CSV
        validador = CSVValidacionService(csv_file)  # Instancia correctamente la clase
        filas = validador.cargar_csv()
        errores = validador.validar()

        if errores:
            return {"estado": "error", "errores": errores}

        # Devolver los datos en formato estructurado para revisión
        return {"estado": "exito", "datos": filas}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el archivo CSV: {str(e)}")
    

@router.post("/rutaCritica/crear_proyecto_desde_csv")
async def crear_proyecto(file: UploadFile, db: AsyncSession = Depends(get_db)):
    # Leer el contenido del archivo CSV
    csv_content = await file.read()
    csv_file = StringIO(csv_content.decode("utf-8"))
    
    # Inicializar el servicio de validación
    validador = CSVValidacionService(csv_file)  # Instancia correctamente la clase
    filas = validador.cargar_csv()
    errores = validador.validar()

    # Si hay errores, devolverlos sin realizar la inserción
    if errores:
        return {"estado": "error", "errores": errores}

    # Si no hay errores, insertar los datos en la base de datos
    return await insertar_datos_proyecto(
        db,
        nombre_proyecto="Proyecto desde CSV",
        descripcion="Importado desde archivo CSV",
        datos=filas
    )
