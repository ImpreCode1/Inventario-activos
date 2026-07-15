from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.activo import Activo
from app.models.estado_activo import EstadoActivo
from app.models.historial_movimiento import HistorialMovimiento
from app.schemas.activo import ActivoCreate, ActivoReasignar, ActivoUpdate


def get_activos(
    db: Session,
    categoria_id: Optional[int] = None,
    ubicacion_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    custodio_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Activo).options(
        joinedload(Activo.categoria),
        joinedload(Activo.ubicacion),
        joinedload(Activo.custodio),
        joinedload(Activo.estado),
    )

    if categoria_id is not None:
        query = query.filter(Activo.categoria_id == categoria_id)
    if ubicacion_id is not None:
        query = query.filter(Activo.ubicacion_id == ubicacion_id)
    if estado_id is not None:
        query = query.filter(Activo.estado_id == estado_id)
    if custodio_id is not None:
        query = query.filter(Activo.custodio_id == custodio_id)
    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Activo.nombre.ilike(like_pattern),
                Activo.codigo_interno.ilike(like_pattern),
                Activo.serial.ilike(like_pattern),
                Activo.marca.ilike(like_pattern),
            )
        )

    return query.offset(skip).limit(limit).all()


def get_activo(db: Session, id: int):
    return (
        db.query(Activo)
        .options(
            joinedload(Activo.categoria),
            joinedload(Activo.ubicacion),
            joinedload(Activo.custodio),
            joinedload(Activo.estado),
        )
        .filter(Activo.id == id)
        .first()
    )


def get_activo_detalle(db: Session, id: int):
    activo = (
        db.query(Activo)
        .options(
            joinedload(Activo.categoria),
            joinedload(Activo.ubicacion),
            joinedload(Activo.custodio),
            joinedload(Activo.estado),
            joinedload(Activo.movimientos),
        )
        .filter(Activo.id == id)
        .first()
    )
    return activo


def create_activo(db: Session, data: ActivoCreate):
    activo = Activo(**data.model_dump())
    db.add(activo)
    db.commit()
    db.refresh(activo)
    return activo


def update_activo(db: Session, id: int, data: ActivoUpdate):
    activo = db.query(Activo).filter(Activo.id == id).first()
    if not activo:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(activo, field, value)
    db.commit()
    db.refresh(activo)
    return activo


def reasignar_activo(db: Session, id: int, data: ActivoReasignar):
    activo = db.query(Activo).filter(Activo.id == id).first()
    if not activo:
        return None

    prev_ubicacion = activo.ubicacion_id
    prev_custodio = activo.custodio_id
    prev_estado = activo.estado_id

    if data.ubicacion_id is not None:
        activo.ubicacion_id = data.ubicacion_id
    if data.custodio_id is not None:
        activo.custodio_id = data.custodio_id
    if data.estado_id is not None:
        activo.estado_id = data.estado_id

    historial = HistorialMovimiento(
        activo_id=activo.id,
        ubicacion_anterior_id=prev_ubicacion if data.ubicacion_id is not None else None,
        ubicacion_nueva_id=data.ubicacion_id if data.ubicacion_id is not None else None,
        custodio_anterior_id=prev_custodio if data.custodio_id is not None else None,
        custodio_nuevo_id=data.custodio_id if data.custodio_id is not None else None,
        estado_anterior_id=prev_estado if data.estado_id is not None else None,
        estado_nuevo_id=data.estado_id if data.estado_id is not None else None,
        usuario_registro_id=data.usuario_registro_id,
        motivo=data.motivo,
    )
    db.add(historial)
    db.commit()
    db.refresh(activo)
    return activo


def delete_activo(db: Session, id: int):
    activo = db.query(Activo).filter(Activo.id == id).first()
    if not activo:
        return None

    estado_baja = db.query(EstadoActivo).filter(EstadoActivo.nombre == "Dado de baja").first()
    if not estado_baja:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Estado 'Dado de baja' no encontrado en el catálogo.",
        )

    prev_estado = activo.estado_id
    activo.estado_id = estado_baja.id

    historial = HistorialMovimiento(
        activo_id=activo.id,
        estado_anterior_id=prev_estado,
        estado_nuevo_id=estado_baja.id,
        motivo="Baja lógica",
    )
    db.add(historial)
    db.commit()
    db.refresh(activo)
    return activo
