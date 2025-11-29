import pytest
from clients.products_client import ProductsClient


class TestUpdateProduct:

    def test_update_product_returns_200(self, products_client: ProductsClient, created_product):
        if created_product is None:
            pytest.skip("Product creation failed")
        
        response = products_client.update_product(
            product_id=created_product["id"],
            name="Updated Product Name",
            price=149.99
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert response_data["name"] == "Updated Product Name"
        assert response_data["price"] == 149.99

    def test_update_product_not_found_returns_404(self, products_client: ProductsClient):
        response = products_client.update_product(
            product_id=999999,
            name="Non-existent Product"
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_update_product_with_invalid_data_returns_422(self, products_client: ProductsClient, created_product):
        if created_product is None:
            pytest.skip("Product creation failed")
        
        response = products_client.patch(f"/products/{created_product['id']}", data={
            "price": "invalid_price"
        })
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
