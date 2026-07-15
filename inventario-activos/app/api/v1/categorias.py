from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.categoria import get_categorias
from app.schemas.categoria import CategoriaResponse

router = APIRouter()


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return get_categorias(db)
