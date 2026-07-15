from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.historial_movimiento import HistorialMovimiento


def get_historial_activo(
    db: Session,
    activo_id: int,
    skip: int = 0,
    limit: int = 50,
):
    return (
        db.query(HistorialMovimiento)
        .options(
            joinedload(HistorialMovimiento.ubicacion_anterior),
            joinedload(HistorialMovimiento.ubicacion_nueva),
            joinedload(HistorialMovimiento.custodio_anterior),
            joinedload(HistorialMovimiento.custodio_nuevo),
            joinedload(HistorialMovimiento.estado_anterior),
            joinedload(HistorialMovimiento.estado_nuevo),
            joinedload(HistorialMovimiento.usuario_registro),
        )
        .filter(HistorialMovimiento.activo_id == activo_id)
        .order_by(HistorialMovimiento.fecha_movimiento.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_historial(
    db: Session,
    activo_id: Optional[int] = None,
    fecha_desde: Optional[str] = None,
    fecha_hasta: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(HistorialMovimiento).options(
        joinedload(HistorialMovimiento.ubicacion_anterior),
        joinedload(HistorialMovimiento.ubicacion_nueva),
        joinedload(HistorialMovimiento.custodio_anterior),
        joinedload(HistorialMovimiento.custodio_nuevo),
        joinedload(HistorialMovimiento.estado_anterior),
        joinedload(HistorialMovimiento.estado_nuevo),
        joinedload(HistorialMovimiento.usuario_registro),
    )

    if activo_id is not None:
        query = query.filter(HistorialMovimiento.activo_id == activo_id)
    if fecha_desde is not None:
        query = query.filter(HistorialMovimiento.fecha_movimiento >= fecha_desde)
    if fecha_hasta is not None:
        query = query.filter(HistorialMovimiento.fecha_movimiento <= fecha_hasta)

    return (
        query.order_by(HistorialMovimiento.fecha_movimiento.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
