from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.estado_activo import get_estados
from app.schemas.estado_activo import EstadoActivoResponse

router = APIRouter()


@router.get("/", response_model=list[EstadoActivoResponse])
def listar_estados(db: Session = Depends(get_db)):
    return get_estados(db)
