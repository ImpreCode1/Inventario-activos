from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Activo(Base):
    __tablename__ = "activos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_interno = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(150), nullable=False)
    marca = Column(String(100), nullable=True)
    modelo = Column(String(100), nullable=True)
    serial = Column(String(150), nullable=True)
    valor = Column(Numeric(12, 2), nullable=True)
    categoria_id = Column(
        Integer, ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False
    )
    ubicacion_id = Column(
        Integer, ForeignKey("ubicaciones.id", ondelete="SET NULL"), nullable=True
    )
    custodio_id = Column(
        Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True
    )
    estado_id = Column(
        Integer, ForeignKey("estados_activo.id", ondelete="RESTRICT"), nullable=False
    )
    fecha_adquisicion = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    categoria = relationship("Categoria")
    ubicacion = relationship("Ubicacion")
    custodio = relationship("Usuario")
    estado = relationship("EstadoActivo")
