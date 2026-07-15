from pydantic import BaseModel


class ConteoEstado(BaseModel):
    estado_id: int
    estado_nombre: str
    total: int


class ConteoCategoria(BaseModel):
    categoria_id: int
    categoria_nombre: str
    total: int


class DashboardResumen(BaseModel):
    por_estado: list[ConteoEstado]
    por_categoria: list[ConteoCategoria]
