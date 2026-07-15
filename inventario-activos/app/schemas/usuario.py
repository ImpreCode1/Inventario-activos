from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    id: int
    hydra_user_id: str
    nombre: str
    email: str
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
