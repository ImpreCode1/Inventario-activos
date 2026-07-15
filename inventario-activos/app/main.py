from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.activos import router as activos_router
from app.api.v1.categorias import router as categorias_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.historial import router as historial_router
from app.api.v1.ubicaciones import router as ubicaciones_router
from app.api.v1.usuarios import router as usuarios_router

app = FastAPI(title="Gestión de Activos - Impresistem S.A.S.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias_router, prefix="/api/v1/categorias", tags=["categorias"])
app.include_router(ubicaciones_router, prefix="/api/v1/ubicaciones", tags=["ubicaciones"])
app.include_router(activos_router, prefix="/api/v1/activos", tags=["activos"])
app.include_router(historial_router, prefix="/api/v1/historial", tags=["historial"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(usuarios_router, prefix="/api/v1/usuarios", tags=["usuarios"])


@app.get("/")
def root():
    return {"message": "Sistema de Gestión de Inventario de Activos - Impresistem S.A.S."}
