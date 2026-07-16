def test_reasignar_activo_genera_historial(client, db):
    from app.models.categoria import Categoria
    from app.models.estado_activo import EstadoActivo
    from app.models.activo import Activo
    from app.models.historial_movimiento import HistorialMovimiento

    cat = Categoria(nombre="Cat")
    disp = EstadoActivo(nombre="Disponible")
    asig = EstadoActivo(nombre="Asignado")
    db.add_all([cat, disp, asig])
    db.commit()

    activo = Activo(codigo_interno="RST-001", nombre="Reasignable", categoria_id=cat.id, estado_id=disp.id)
    db.add(activo)
    db.commit()

    response = client.patch(f"/api/v1/activos/{activo.id}/reasignar", json={
        "estado_id": asig.id,
        "motivo": "Prueba de reasignación",
    })
    assert response.status_code == 200
    assert response.json()["estado_id"] == asig.id

    historiales = db.query(HistorialMovimiento).filter(
        HistorialMovimiento.activo_id == activo.id
    ).all()
    assert len(historiales) == 1
    h = historiales[0]
    assert h.estado_anterior_id == disp.id
    assert h.estado_nuevo_id == asig.id
    assert h.motivo == "Prueba de reasignación"
    assert h.ubicacion_anterior_id is None
    assert h.custodio_anterior_id is None


def test_baja_logica_genera_historial(client, db):
    from app.models.categoria import Categoria
    from app.models.estado_activo import EstadoActivo
    from app.models.activo import Activo
    from app.models.historial_movimiento import HistorialMovimiento

    cat = Categoria(nombre="Cat")
    disp = EstadoActivo(nombre="Disponible")
    baja = EstadoActivo(nombre="Dado de baja")
    db.add_all([cat, disp, baja])
    db.commit()

    activo = Activo(codigo_interno="BAJ-001", nombre="Para bajar", categoria_id=cat.id, estado_id=disp.id)
    db.add(activo)
    db.commit()

    response = client.delete(f"/api/v1/activos/{activo.id}")
    assert response.status_code == 200
    assert response.json()["estado_id"] == baja.id

    historiales = db.query(HistorialMovimiento).filter(
        HistorialMovimiento.activo_id == activo.id
    ).all()
    assert len(historiales) == 1
    assert historiales[0].estado_anterior_id == disp.id
    assert historiales[0].estado_nuevo_id == baja.id
    assert historiales[0].motivo == "Baja lógica"
