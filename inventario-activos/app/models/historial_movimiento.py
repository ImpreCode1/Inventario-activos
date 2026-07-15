from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class HistorialMovimiento(Base):
    __tablename__ = "historial_movimientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activo_id = Column(
        Integer, ForeignKey("activos.id", ondelete="CASCADE"), nullable=False
    )
    ubicacion_anterior_id = Column(
        Integer, ForeignKey("ubicaciones.id"), nullable=True
    )
    ubicacion_nueva_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    custodio_anterior_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    custodio_nuevo_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    estado_anterior_id = Column(
        Integer, ForeignKey("estados_activo.id"), nullable=True
    )
    estado_nuevo_id = Column(Integer, ForeignKey("estados_activo.id"), nullable=True)
    usuario_registro_id = Column(
        Integer, ForeignKey("usuarios.id"), nullable=True
    )
    motivo = Column(Text, nullable=True)
    fecha_movimiento = Column(DateTime, server_default=func.now())

    activo = relationship("Activo", backref="movimientos")
    ubicacion_anterior = relationship(
        "Ubicacion", foreign_keys=[ubicacion_anterior_id]
    )
    ubicacion_nueva = relationship("Ubicacion", foreign_keys=[ubicacion_nueva_id])
    custodio_anterior = relationship(
        "Usuario", foreign_keys=[custodio_anterior_id]
    )
    custodio_nuevo = relationship("Usuario", foreign_keys=[custodio_nuevo_id])
    estado_anterior = relationship(
        "EstadoActivo", foreign_keys=[estado_anterior_id]
    )
    estado_nuevo = relationship("EstadoActivo", foreign_keys=[estado_nuevo_id])
    usuario_registro = relationship("Usuario", foreign_keys=[usuario_registro_id])
