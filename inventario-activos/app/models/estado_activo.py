from sqlalchemy import Column, Integer, String

from app.core.database import Base


class EstadoActivo(Base):
    __tablename__ = "estados_activo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
