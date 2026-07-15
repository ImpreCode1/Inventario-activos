from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UbicacionCreate(BaseModel):
    nombre: str
    ubicacion_padre_id: Optional[int] = None
    nivel: Optional[str] = None


class UbicacionUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion_padre_id: Optional[int] = None
    nivel: Optional[str] = None
    activo: Optional[bool] = None


class UbicacionResponse(BaseModel):
    id: int
    nombre: str
    ubicacion_padre_id: Optional[int] = None
    nivel: Optional[str] = None
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UbicacionArbol(UbicacionResponse):
    hijos: list["UbicacionArbol"] = []
