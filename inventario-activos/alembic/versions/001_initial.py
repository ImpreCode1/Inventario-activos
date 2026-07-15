"""initial migration

Revision ID: 001
Revises:
Create Date: 2026-07-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_table(
        "ubicaciones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("ubicacion_padre_id", sa.Integer(), nullable=True),
        sa.Column("nivel", sa.String(50), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["ubicacion_padre_id"],
            ["ubicaciones.id"],
            ondelete="RESTRICT",
        ),
    )
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("hydra_user_id", sa.String(255), nullable=False),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("email", sa.String(150), nullable=False),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hydra_user_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "estados_activo",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_table(
        "activos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("codigo_interno", sa.String(50), nullable=False),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("marca", sa.String(100), nullable=True),
        sa.Column("modelo", sa.String(100), nullable=True),
        sa.Column("serial", sa.String(150), nullable=True),
        sa.Column("valor", sa.Numeric(12, 2), nullable=True),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.Column("ubicacion_id", sa.Integer(), nullable=True),
        sa.Column("custodio_id", sa.Integer(), nullable=True),
        sa.Column("estado_id", sa.Integer(), nullable=False),
        sa.Column("fecha_adquisicion", sa.Date(), nullable=True),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_interno"),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["ubicacion_id"], ["ubicaciones.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["custodio_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["estado_id"], ["estados_activo.id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "historial_movimientos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("activo_id", sa.Integer(), nullable=False),
        sa.Column("ubicacion_anterior_id", sa.Integer(), nullable=True),
        sa.Column("ubicacion_nueva_id", sa.Integer(), nullable=True),
        sa.Column("custodio_anterior_id", sa.Integer(), nullable=True),
        sa.Column("custodio_nuevo_id", sa.Integer(), nullable=True),
        sa.Column("estado_anterior_id", sa.Integer(), nullable=True),
        sa.Column("estado_nuevo_id", sa.Integer(), nullable=True),
        sa.Column("usuario_registro_id", sa.Integer(), nullable=True),
        sa.Column("motivo", sa.Text(), nullable=True),
        sa.Column("fecha_movimiento", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["activo_id"], ["activos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["ubicacion_anterior_id"], ["ubicaciones.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["ubicacion_nueva_id"], ["ubicaciones.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["custodio_anterior_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["custodio_nuevo_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["estado_anterior_id"], ["estados_activo.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["estado_nuevo_id"], ["estados_activo.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["usuario_registro_id"], ["usuarios.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("historial_movimientos")
    op.drop_table("activos")
    op.drop_table("estados_activo")
    op.drop_table("usuarios")
    op.drop_table("ubicaciones")
    op.drop_table("categorias")
