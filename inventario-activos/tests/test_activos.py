def test_crear_activo(client, db):
    from app.models.categoria import Categoria
    from app.models.estado_activo import EstadoActivo

    cat = Categoria(nombre="Test Cat")
    est = EstadoActivo(nombre="Disponible")
    db.add_all([cat, est])
    db.commit()

    response = client.post("/api/v1/activos", json={
        "codigo_interno": "TST-001",
        "nombre": "Activo de prueba",
        "categoria_id": cat.id,
        "estado_id": est.id,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["codigo_interno"] == "TST-001"


def test_crear_activo_sin_codigo(client):
    response = client.post("/api/v1/activos", json={
        "codigo_interno": "",
        "nombre": "Test",
        "categoria_id": 1,
        "estado_id": 1,
    })
    assert response.status_code == 422


def test_crear_activo_nombre_corto(client):
    response = client.post("/api/v1/activos", json={
        "codigo_interno": "TST-002",
        "nombre": "AB",
        "categoria_id": 1,
        "estado_id": 1,
    })
    assert response.status_code == 422


def test_listar_activos_paginado(client, db):
    from app.models.categoria import Categoria
    from app.models.estado_activo import EstadoActivo
    from app.models.activo import Activo

    cat = Categoria(nombre="Cat")
    est = EstadoActivo(nombre="Disponible")
    db.add_all([cat, est])
    db.commit()

    for i in range(5):
        db.add(Activo(codigo_interno=f"TST-{i:03d}", nombre=f"Activo {i}", categoria_id=cat.id, estado_id=est.id))
    db.commit()

    response = client.get("/api/v1/activos?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
