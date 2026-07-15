from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ubicacion import (
    create_ubicacion,
    delete_ubicacion,
    get_ubicacion,
    get_ubicacion_arbol,
    get_ubicaciones,
    update_ubicacion,
)
from app.schemas.ubicacion import (
    UbicacionArbol,
    UbicacionCreate,
    UbicacionResponse,
    UbicacionUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[UbicacionResponse])
def listar_ubicaciones(db: Session = Depends(get_db)):
    return get_ubicaciones(db)


@router.get("/arbol", response_model=list[UbicacionArbol])
def arbol_ubicaciones(db: Session = Depends(get_db)):
    return get_ubicacion_arbol(db)


@router.post("/", response_model=UbicacionResponse, status_code=201)
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_db)):
    return create_ubicacion(db, data)


@router.get("/{id}", response_model=UbicacionResponse)
def obtener_ubicacion(id: int, db: Session = Depends(get_db)):
    ubicacion = get_ubicacion(db, id)
    if not ubicacion:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
    return ubicacion


@router.put("/{id}", response_model=UbicacionResponse)
def editar_ubicacion(id: int, data: UbicacionUpdate, db: Session = Depends(get_db)):
    ubicacion = update_ubicacion(db, id, data)
    if not ubicacion:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
    return ubicacion


@router.delete("/{id}", response_model=UbicacionResponse)
def desactivar_ubicacion(id: int, db: Session = Depends(get_db)):
    ubicacion = delete_ubicacion(db, id)
    if not ubicacion:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
    return ubicacion
