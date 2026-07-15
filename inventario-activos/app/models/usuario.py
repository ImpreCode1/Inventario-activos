from sqlalchemy import Boolean, Column, Integer, String, DateTime, func

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hydra_user_id = Column(String(255), nullable=False, unique=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
