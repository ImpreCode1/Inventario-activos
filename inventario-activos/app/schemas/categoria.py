from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
