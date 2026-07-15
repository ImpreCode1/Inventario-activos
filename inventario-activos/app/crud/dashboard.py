from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activo import Activo
from app.models.estado_activo import EstadoActivo
from app.models.categoria import Categoria


def get_resumen(db: Session):
    por_estado = (
        db.query(
            Activo.estado_id,
            EstadoActivo.nombre.label("estado_nombre"),
            func.count(Activo.id).label("total"),
        )
        .join(EstadoActivo, Activo.estado_id == EstadoActivo.id)
        .group_by(Activo.estado_id, EstadoActivo.nombre)
        .all()
    )

    por_categoria = (
        db.query(
            Activo.categoria_id,
            Categoria.nombre.label("categoria_nombre"),
            func.count(Activo.id).label("total"),
        )
        .join(Categoria, Activo.categoria_id == Categoria.id)
        .group_by(Activo.categoria_id, Categoria.nombre)
        .all()
    )

    return {
        "por_estado": [
            {"estado_id": r.estado_id, "estado_nombre": r.estado_nombre, "total": r.total}
            for r in por_estado
        ],
        "por_categoria": [
            {"categoria_id": r.categoria_id, "categoria_nombre": r.categoria_nombre, "total": r.total}
            for r in por_categoria
        ],
    }


def get_activos_por_custodio(db: Session, usuario_id: int):
    return (
        db.query(Activo)
        .filter(Activo.custodio_id == usuario_id)
        .all()
    )
