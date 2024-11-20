# app/main.py
from fastapi import FastAPI
from .api import endpoints  # Importa el módulo con los endpoints
from .api import csv_routes

app = FastAPI()

# Incluye las rutas de la API
app.include_router(endpoints.router)
app.include_router(csv_routes.router)

