def test_listar_categorias_vacio(client):
    response = client.get("/api/v1/categorias")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_categorias_con_datos(client, db):
    from app.models.categoria import Categoria
    db.add(Categoria(nombre="Equipos de Cómputo", descripcion="Test"))
    db.commit()

    response = client.get("/api/v1/categorias")
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Equipos de Cómputo"
