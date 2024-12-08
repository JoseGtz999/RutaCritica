# app/main.py
from fastapi import FastAPI
from .api import proyecto_routes  # Importa el módulo con los endpoints
from .api import csv_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Incluye las rutas de la API
app.include_router(proyecto_routes.router)
app.include_router(csv_routes.router)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde localhost:35405
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
async def root():
    return {"message": "Hello World"}