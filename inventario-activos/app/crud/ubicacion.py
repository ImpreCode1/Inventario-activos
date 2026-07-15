from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionArbol, UbicacionCreate, UbicacionUpdate


def get_ubicaciones(db: Session):
    return db.query(Ubicacion).filter(Ubicacion.activo == True).all()


def get_ubicacion_arbol(db: Session):
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.activo == True).all()
    mapa: dict[int, UbicacionArbol] = {}
    raices: list[UbicacionArbol] = []

    for u in ubicaciones:
        nodo = UbicacionArbol(
            id=u.id,
            nombre=u.nombre,
            ubicacion_padre_id=u.ubicacion_padre_id,
            nivel=u.nivel,
            activo=u.activo,
            created_at=u.created_at,
            hijos=[],
        )
        mapa[u.id] = nodo

    for nodo in mapa.values():
        padre_id = nodo.ubicacion_padre_id
        if padre_id and padre_id in mapa:
            mapa[padre_id].hijos.append(nodo)
        else:
            raices.append(nodo)

    return raices


def get_ubicacion(db: Session, id: int):
    return db.query(Ubicacion).filter(Ubicacion.id == id, Ubicacion.activo == True).first()


def create_ubicacion(db: Session, data: UbicacionCreate):
    ubicacion = Ubicacion(**data.model_dump())
    db.add(ubicacion)
    db.commit()
    db.refresh(ubicacion)
    return ubicacion


def update_ubicacion(db: Session, id: int, data: UbicacionUpdate):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == id, Ubicacion.activo == True).first()
    if not ubicacion:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ubicacion, field, value)
    db.commit()
    db.refresh(ubicacion)
    return ubicacion


def delete_ubicacion(db: Session, id: int):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == id, Ubicacion.activo == True).first()
    if not ubicacion:
        return None

    hijos_activos = (
        db.query(Ubicacion)
        .filter(Ubicacion.ubicacion_padre_id == id, Ubicacion.activo == True)
        .count()
    )
    if hijos_activos > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede desactivar la ubicación porque tiene ubicaciones hijas activas.",
        )

    from app.models.activo import Activo

    activos_asignados = (
        db.query(Activo)
        .filter(Activo.ubicacion_id == id)
        .count()
    )
    if activos_asignados > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede desactivar la ubicación porque tiene activos asignados.",
        )

    ubicacion.activo = False
    db.commit()
    return ubicacion
