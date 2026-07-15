from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.dashboard import get_resumen
from app.schemas.dashboard import DashboardResumen

router = APIRouter()


@router.get("/resumen", response_model=DashboardResumen)
def resumen_dashboard(db: Session = Depends(get_db)):
    return get_resumen(db)
