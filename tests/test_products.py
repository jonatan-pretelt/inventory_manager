def test_create_product_success(client):
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "sku": "SKU-123",
            "price": 10.5,
            "quantity": 4,
            "category": "test"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "SKU-123"


# def test_duplicate_error(client):
#     client.post(
#         "/products/",
#         json={
#             "name": "Test Product",
#             "sku": "SKU-123",
#             "price": 10.5,
#             "quantity": 4,
#             "category": "test"
#         }
#     )

#     response = client.post(
#         "/products/",
#         json={
#             "name": "Test Product",
#             "sku": "SKU-123",
#             "price": 10.5,
#             "quantity": 4,
#             "category": "test"
#         }
#     )
#     assert response.status_code == 409
#     data = response.json()
#     assert data["sku"] == "SKU-123"

def test_duplicate_sku_returns_error(client):
    payload = {
        "name": "Test Product",
        "sku": "SKU-123",
        "price": 10.5,
        "quantity": 4,
        "category": "test"
    }

    # First request should succeed
    response1 = client.post("/products/", json=payload)
    assert response1.status_code == 200

    # Second request should trigger duplicate logic
    response2 = client.post("/products/", json=payload)

    assert response2.status_code == 409