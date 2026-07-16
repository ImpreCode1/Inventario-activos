def test_dashboard_resumen_vacio(client):
    response = client.get("/api/v1/dashboard/resumen")
    assert response.status_code == 200
    data = response.json()
    assert data["por_estado"] == []
    assert data["por_categoria"] == []


def test_dashboard_resumen_con_datos(client, db):
    from app.models.categoria import Categoria
    from app.models.estado_activo import EstadoActivo
    from app.models.activo import Activo

    cat = Categoria(nombre="Equipos")
    disp = EstadoActivo(nombre="Disponible")
    asig = EstadoActivo(nombre="Asignado")
    db.add_all([cat, disp, asig])
    db.commit()

    for _ in range(3):
        db.add(Activo(codigo_interno=f"DD-{_}", nombre=f"D {_}", categoria_id=cat.id, estado_id=disp.id))
    db.commit()

    response = client.get("/api/v1/dashboard/resumen")
    data = response.json()
    assert len(data["por_estado"]) == 1
    assert data["por_estado"][0]["total"] == 3
    assert len(data["por_categoria"]) == 1
    assert data["por_categoria"][0]["total"] == 3
