from sqlalchemy.orm import Session

from app.models.estado_activo import EstadoActivo


def get_estados(db: Session):
    return db.query(EstadoActivo).all()
