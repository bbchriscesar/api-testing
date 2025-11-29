import pytest
from clients.products_client import ProductsClient


class TestGetProducts:

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_get_products_returns_200(self, products_client: ProductsClient):
        response = products_client.get_products()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert isinstance(response_data, list), "Response should be a list of products"

    @pytest.mark.regression
    def test_get_products_without_api_key_returns_200(self):
        client = ProductsClient(api_key="")
        
        response = client.get_products()
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        client.close()

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_get_products_with_invalid_api_key_returns_403(self):
        client = ProductsClient(api_key="invalid-api-key-12345")
        
        response = client.get_products()
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        client.close()

    @pytest.mark.regression
    def test_get_product_not_found_returns_404(self, products_client: ProductsClient):
        response = products_client.get_product(product_id=999999)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
