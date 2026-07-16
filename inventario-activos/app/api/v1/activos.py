from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.activo import (
    create_activo,
    delete_activo,
    get_activo_detalle,
    get_activos,
    reasignar_activo,
    update_activo,
)
from app.crud.historial import get_historial_activo
from app.schemas.activo import (
    ActivoCreate,
    ActivoDetailResponse,
    ActivoReasignar,
    ActivoResponse,
    ActivoUpdate,
)
from app.schemas.historial import HistorialResponse
from app.schemas.pagination import PaginatedResponse

router = APIRouter()


@router.get("/{id}/historial", response_model=list[HistorialResponse])
def historial_activo(
    id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return get_historial_activo(db, id, skip=skip, limit=limit)


@router.get("/", response_model=PaginatedResponse[ActivoResponse])
def listar_activos(
    categoria_id: Optional[int] = Query(None),
    ubicacion_id: Optional[int] = Query(None),
    estado_id: Optional[int] = Query(None),
    custodio_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return get_activos(
        db,
        categoria_id=categoria_id,
        ubicacion_id=ubicacion_id,
        estado_id=estado_id,
        custodio_id=custodio_id,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{id}", response_model=ActivoDetailResponse)
def obtener_activo(id: int, db: Session = Depends(get_db)):
    activo = get_activo_detalle(db, id)
    if not activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
    return activo


@router.post("/", response_model=ActivoResponse, status_code=201)
def crear_activo(data: ActivoCreate, db: Session = Depends(get_db)):
    return create_activo(db, data)


@router.put("/{id}", response_model=ActivoResponse)
def editar_activo(id: int, data: ActivoUpdate, db: Session = Depends(get_db)):
    activo = update_activo(db, id, data)
    if not activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
    return activo


@router.patch("/{id}/reasignar", response_model=ActivoResponse)
def reasignar_activo_endpoint(id: int, data: ActivoReasignar, db: Session = Depends(get_db)):
    activo = reasignar_activo(db, id, data)
    if not activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
    return activo


@router.delete("/{id}", response_model=ActivoResponse)
def dar_de_baja_activo(id: int, db: Session = Depends(get_db)):
    activo = delete_activo(db, id)
    if not activo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activo no encontrado")
    return activo
