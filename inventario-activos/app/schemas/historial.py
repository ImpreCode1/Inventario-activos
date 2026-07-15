from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.ubicacion import UbicacionResponse
from app.schemas.usuario import UsuarioResponse
from app.schemas.estado_activo import EstadoActivoResponse


class HistorialResponse(BaseModel):
    id: int
    activo_id: int
    ubicacion_anterior_id: Optional[int] = None
    ubicacion_nueva_id: Optional[int] = None
    custodio_anterior_id: Optional[int] = None
    custodio_nuevo_id: Optional[int] = None
    estado_anterior_id: Optional[int] = None
    estado_nuevo_id: Optional[int] = None
    usuario_registro_id: Optional[int] = None
    motivo: Optional[str] = None
    fecha_movimiento: datetime

    ubicacion_anterior: Optional[UbicacionResponse] = None
    ubicacion_nueva: Optional[UbicacionResponse] = None
    custodio_anterior: Optional[UsuarioResponse] = None
    custodio_nuevo: Optional[UsuarioResponse] = None
    estado_anterior: Optional[EstadoActivoResponse] = None
    estado_nuevo: Optional[EstadoActivoResponse] = None
    usuario_registro: Optional[UsuarioResponse] = None

    model_config = {"from_attributes": True}
