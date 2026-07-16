def test_arbol_ubicaciones_vacio(client):
    response = client.get("/api/v1/ubicaciones/arbol")
    assert response.status_code == 200
    assert response.json() == []


def test_arbol_ubicaciones_con_datos(client, db):
    from app.models.ubicacion import Ubicacion

    sede = Ubicacion(nombre="Sede Principal", nivel="sede")
    db.add(sede)
    db.commit()

    area = Ubicacion(nombre="Administración", ubicacion_padre_id=sede.id, nivel="area")
    db.add(area)
    db.commit()

    response = client.get("/api/v1/ubicaciones/arbol")
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Sede Principal"
    assert len(data[0]["hijos"]) == 1
    assert data[0]["hijos"][0]["nombre"] == "Administración"


def test_eliminar_ubicacion_con_hijos_rechaza(client, db):
    from app.models.ubicacion import Ubicacion

    sede = Ubicacion(nombre="Sede", nivel="sede")
    db.add(sede)
    db.commit()
    area = Ubicacion(nombre="Área", ubicacion_padre_id=sede.id, nivel="area")
    db.add(area)
    db.commit()

    response = client.delete(f"/api/v1/ubicaciones/{sede.id}")
    assert response.status_code == 400
    assert "hij" in response.json()["detail"].lower()
