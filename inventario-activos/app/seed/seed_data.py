from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.categoria import Categoria
from app.models.ubicacion import Ubicacion
from app.models.usuario import Usuario
from app.models.estado_activo import EstadoActivo
from app.models.activo import Activo


def seed_database(db: Session):
    if db.query(Categoria).first():
        return

    categorias = [
        Categoria(nombre="Equipos de Cómputo", descripcion="Laptops, desktops, servidores y periféricos"),
        Categoria(nombre="Mobiliario", descripcion="Escritorios, sillas, estanterías y muebles en general"),
        Categoria(nombre="Herramientas", descripcion="Herramientas manuales, eléctricas y de medición"),
    ]
    db.add_all(categorias)
    db.flush()

    estados = [
        EstadoActivo(nombre="Disponible"),
        EstadoActivo(nombre="Asignado"),
        EstadoActivo(nombre="En mantenimiento"),
        EstadoActivo(nombre="Dado de baja"),
    ]
    db.add_all(estados)
    db.flush()

    sede_ppal = Ubicacion(nombre="Sede Principal", nivel="sede", activo=True)
    sede_sec = Ubicacion(nombre="Sede Secundaria", nivel="sede", activo=True)
    db.add_all([sede_ppal, sede_sec])
    db.flush()

    areas_ppal = [
        Ubicacion(nombre="Administración", ubicacion_padre_id=sede_ppal.id, nivel="area", activo=True),
        Ubicacion(nombre="Producción", ubicacion_padre_id=sede_ppal.id, nivel="area", activo=True),
    ]
    areas_sec = [
        Ubicacion(nombre="Bodega", ubicacion_padre_id=sede_sec.id, nivel="area", activo=True),
        Ubicacion(nombre="Taller", ubicacion_padre_id=sede_sec.id, nivel="area", activo=True),
    ]
    db.add_all(areas_ppal + areas_sec)
    db.flush()

    usuario = Usuario(
        hydra_user_id="usr-seed-001",
        nombre="Carlos Pérez",
        email="carlos.perez@impresistem.com",
        activo=True,
    )
    db.add(usuario)
    db.flush()

    activos = [
        Activo(
            codigo_interno="EQ-001",
            nombre="Laptop Dell Latitude 5540",
            marca="Dell",
            modelo="Latitude 5540",
            serial="SN-DELL-001",
            valor=4500000.00,
            categoria_id=categorias[0].id,
            ubicacion_id=areas_ppal[0].id,
            custodio_id=usuario.id,
            estado_id=estados[1].id,
            fecha_adquisicion="2025-03-15",
            observaciones="Equipo asignado a administración",
        ),
        Activo(
            codigo_interno="EQ-002",
            nombre="Servidor HP ProLiant DL380",
            marca="HP",
            modelo="ProLiant DL380 Gen10",
            serial="SN-HP-002",
            valor=12500000.00,
            categoria_id=categorias[0].id,
            ubicacion_id=areas_ppal[1].id,
            custodio_id=None,
            estado_id=estados[0].id,
            fecha_adquisicion="2025-01-20",
            observaciones="Servidor de producción",
        ),
        Activo(
            codigo_interno="MB-001",
            nombre="Escritorio ergonómico",
            marca="Ofimuebles",
            modelo="E-2000",
            serial=None,
            valor=850000.00,
            categoria_id=categorias[1].id,
            ubicacion_id=areas_ppal[0].id,
            custodio_id=None,
            estado_id=estados[0].id,
            fecha_adquisicion="2024-11-01",
            observaciones=None,
        ),
        Activo(
            codigo_interno="HR-001",
            nombre="Taladro inalámbrico DeWalt",
            marca="DeWalt",
            modelo="DCD791D2",
            serial="SN-DEW-003",
            valor=620000.00,
            categoria_id=categorias[2].id,
            ubicacion_id=areas_sec[1].id,
            custodio_id=None,
            estado_id=estados[2].id,
            fecha_adquisicion="2025-06-10",
            observaciones="En mantenimiento preventivo",
        ),
        Activo(
            codigo_interno="EQ-003",
            nombre="Monitor LG 27\" 4K",
            marca="LG",
            modelo="27UK850-W",
            serial="SN-LG-004",
            valor=1800000.00,
            categoria_id=categorias[0].id,
            ubicacion_id=areas_ppal[0].id,
            custodio_id=usuario.id,
            estado_id=estados[1].id,
            fecha_adquisicion="2025-08-01",
            observaciones="Monitor asignado con laptop",
        ),
    ]
    db.add_all(activos)
    db.commit()


def run():
    db = SessionLocal()
    try:
        seed_database(db)
        print("Seed data inserted successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
