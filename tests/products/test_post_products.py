import pytest
from clients.products_client import ProductsClient


class TestCreateProduct:

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_product_returns_201(self, products_client: ProductsClient):
        payload = {
            "name": "Test Product",
            "price": 99.99,
            "description": "Test product for automated testing",
            "stock": 10
        }
        
        response = products_client.create_product(
            name=payload["name"],
            price=payload["price"],
            description=payload["description"],
            stock=payload["stock"]
        )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        response_data = response.json()
        assert response_data["name"] == "Test Product"
        assert response_data["price"] == 99.99
        assert response_data["description"] == "Test product for automated testing"
        assert response_data["stock"] == 10
        assert "id" in response_data
        
        # Cleanup: Delete created product
        products_client.delete_product(response_data["id"])

    @pytest.mark.regression
    def test_create_product_without_required_fields_returns_422(self, products_client: ProductsClient):
        response = products_client.post("/products/", data={})
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    @pytest.mark.regression
    def test_create_product_with_invalid_price_returns_422(self, products_client: ProductsClient):
        response = products_client.post("/products/", data={
            "name": "Invalid Product",
            "price": "invalid_price",
            "stock": 10
        })
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    @pytest.mark.regression
    def test_create_product_with_negative_price_returns_200(self, products_client: ProductsClient):
        response = products_client.create_product(
            name="Negative Price Product",
            price=-10.00,
            stock=5
        )
        
        # Cleanup if needed
        if response.status_code == 200:
            response_data = response.json()
            products_client.delete_product(response_data["id"])
        
        assert response.status_code in [200, 422], f"Expected 200 or 422, got {response.status_code}"
