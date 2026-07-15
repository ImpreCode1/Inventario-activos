from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.dashboard import get_activos_por_custodio
from app.schemas.activo import ActivoResponse

router = APIRouter()


@router.get("/{id}/activos", response_model=list[ActivoResponse])
def activos_por_custodio(id: int, db: Session = Depends(get_db)):
    activos = get_activos_por_custodio(db, id)
    if not activos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no tiene activos asignados")
    return activos
