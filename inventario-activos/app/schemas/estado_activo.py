from pydantic import BaseModel


class EstadoActivoResponse(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}
