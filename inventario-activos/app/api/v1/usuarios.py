from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.dashboard import get_activos_por_custodio
from app.crud.usuario import get_usuarios
from app.schemas.activo import ActivoResponse
from app.schemas.usuario import UsuarioResponse

router = APIRouter()


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return get_usuarios(db)


@router.get("/{id}/activos", response_model=list[ActivoResponse])
def activos_por_custodio(id: int, db: Session = Depends(get_db)):
    activos = get_activos_por_custodio(db, id)
    if not activos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no tiene activos asignados")
    return activos
