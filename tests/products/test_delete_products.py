import pytest
from clients.products_client import ProductsClient


class TestDeleteProduct:

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_delete_product_returns_200(self, products_client: ProductsClient):
        # Create a product to delete
        create_response = products_client.post("/products/", data={
            "name": "Product to Delete",
            "price": 50.00,
            "stock": 5,
            "description": "Test product for deletion",
            "image_url": "https://example.com/image.jpg"
        })
        
        assert create_response.status_code == 201, f"Setup failed: Expected 201, got {create_response.status_code}"
        
        product_id = create_response.json()["id"]
        
        response = products_client.delete_product(product_id)
        
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        
        # Verify product no longer exists
        get_response = products_client.get_product(product_id)
        assert get_response.status_code == 404, "Product should not exist after deletion"

    @pytest.mark.regression
    def test_delete_product_not_found_returns_404(self, products_client: ProductsClient):
        response = products_client.delete_product(product_id=999999)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
