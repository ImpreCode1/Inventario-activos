from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator

from app.schemas.categoria import CategoriaResponse
from app.schemas.historial import HistorialResponse
from app.schemas.ubicacion import UbicacionResponse
from app.schemas.usuario import UsuarioResponse
from app.schemas.estado_activo import EstadoActivoResponse


class ActivoCreate(BaseModel):
    codigo_interno: str
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serial: Optional[str] = None
    valor: Optional[Decimal] = None
    categoria_id: int
    ubicacion_id: Optional[int] = None
    custodio_id: Optional[int] = None
    estado_id: int
    fecha_adquisicion: Optional[date] = None
    observaciones: Optional[str] = None

    @field_validator("codigo_interno")
    @classmethod
    def codigo_no_vacio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El código interno no puede estar vacío")
        return v.strip()

    @field_validator("nombre")
    @classmethod
    def nombre_min_length(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return v.strip()

    @field_validator("valor")
    @classmethod
    def valor_positivo(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser positivo")
        return v


class ActivoUpdate(BaseModel):
    codigo_interno: Optional[str] = None
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serial: Optional[str] = None
    valor: Optional[Decimal] = None
    categoria_id: Optional[int] = None
    ubicacion_id: Optional[int] = None
    custodio_id: Optional[int] = None
    estado_id: Optional[int] = None
    fecha_adquisicion: Optional[date] = None
    observaciones: Optional[str] = None

    @field_validator("codigo_interno")
    @classmethod
    def codigo_no_vacio(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El código interno no puede estar vacío")
        return v.strip() if v else v

    @field_validator("nombre")
    @classmethod
    def nombre_min_length(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return v.strip() if v else v

    @field_validator("valor")
    @classmethod
    def valor_positivo(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None and v <= 0:
            raise ValueError("El valor debe ser positivo")
        return v


class ActivoReasignar(BaseModel):
    ubicacion_id: Optional[int] = None
    custodio_id: Optional[int] = None
    estado_id: Optional[int] = None
    motivo: Optional[str] = None
    usuario_registro_id: Optional[int] = None


class ActivoResponse(BaseModel):
    id: int
    codigo_interno: str
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serial: Optional[str] = None
    valor: Optional[Decimal] = None
    categoria_id: int
    ubicacion_id: Optional[int] = None
    custodio_id: Optional[int] = None
    estado_id: int
    fecha_adquisicion: Optional[date] = None
    observaciones: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    categoria: Optional[CategoriaResponse] = None
    ubicacion: Optional[UbicacionResponse] = None
    custodio: Optional[UsuarioResponse] = None
    estado: Optional[EstadoActivoResponse] = None

    model_config = {"from_attributes": True}


class ActivoDetailResponse(ActivoResponse):
    movimientos: list[HistorialResponse] = []

    model_config = {"from_attributes": True}
