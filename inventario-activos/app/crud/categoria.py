from sqlalchemy.orm import Session

from app.models.categoria import Categoria


def get_categorias(db: Session):
    return db.query(Categoria).filter(Categoria.activo == True).all()
