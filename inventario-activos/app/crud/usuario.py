from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def get_usuarios(db: Session):
    return db.query(Usuario).filter(Usuario.activo == True).all()
