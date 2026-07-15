from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ubicacion_padre_id = Column(
        Integer, ForeignKey("ubicaciones.id", ondelete="RESTRICT"), nullable=True
    )
    nivel = Column(String(50), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    padre = relationship("Ubicacion", remote_side="Ubicacion.id", backref="hijos")
