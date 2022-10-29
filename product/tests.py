from fastapi.testclient import TestClient


def test_create_product(client: TestClient):
    user = client.post(
        "/user/register",
        json={
            "username": "test",
            "password": "test",
            "email": "test@email.com",
        },
    )
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.post(
        "/product/create",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "product 1",
            "price": 100.0
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "Product product 1 created successfully"
    }


def test_get_product(client: TestClient):
    response = client.post("/product/info", json={"name": "Product 1"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "product 1",
        "price": 100.0,
        "is_active": True
    }


def test_list_products(client: TestClient):
    response = client.get("/product/list")
    print(response.json())
    assert response.status_code == 200
    assert response.json()[0] == {
        "id": 1,
        "name": "product 1",
        "price": 100.0,
        "is_active": True
    }


def test_list_active_products(client: TestClient):
    response = client.get("/product/list_active")
    assert response.status_code == 200
    assert response.json()[0] == {
        "id": 1,
        "name": "product 1",
        "price": 100.0,
        "is_active": True
    }


def test_add_product_to_shopping_cart(client: TestClient):
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.post(
        "/product/add-to-cart",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product added to shopping cart successfully"
    }


def test_get_current_shopping_cart(client: TestClient):
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.get(
        "/product/shopping-cart",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()[0] == {
        'paid': False,
        'id': 1,
        'shopping_cart_id': 1,
        'product_id': 1,
        'user_id': 1
    }

def test_remove_product_from_shopping_cart(client: TestClient):
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.post(
        "/product/remove-from-cart",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product removed from shopping cart successfully"
    }

def test_update_product(client: TestClient):
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.put(
        "/product/update",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "product 1",
            "price": 200.0
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product product 1 updated successfully; new price: 200.0"
    }

def test_delete_product(client: TestClient):
    token = client.post(
        "/user/token",
        data={
            "username": "test",
            "password": "test"
        },
    ).json()["access_token"]
    response = client.delete(
        "/product/delete",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "product 1"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product product 1 deleted successfully"
    }