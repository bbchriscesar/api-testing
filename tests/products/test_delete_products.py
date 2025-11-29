import pytest
import allure
from clients.products_client import ProductsClient


@allure.epic("Products API")
@allure.feature("DELETE Products")
class TestDeleteProduct:

    @allure.story("Delete Product")
    @allure.title("Delete existing product returns 204 No Content")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_delete_product_returns_200(self, products_client: ProductsClient):
        with allure.step("Create a product to delete"):
            create_response = products_client.post("/products/", data={
                "name": "Product to Delete",
                "price": 50.00,
                "stock": 5,
                "description": "Test product for deletion",
                "image_url": "https://example.com/image.jpg"
            })
            allure.attach(str(create_response.json()), name="Created Product", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Verify product was created successfully"):
            assert create_response.status_code == 201, f"Setup failed: Expected 201, got {create_response.status_code}"
        
        product_id = create_response.json()["id"]
        
        with allure.step(f"Send DELETE request for product {product_id}"):
            response = products_client.delete_product(product_id)
        
        with allure.step("Verify response status code is 204"):
            assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        
        with allure.step("Verify product no longer exists"):
            get_response = products_client.get_product(product_id)
            assert get_response.status_code == 404, "Product should not exist after deletion"

    @allure.story("Delete Product")
    @allure.title("Delete non-existent product returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_delete_product_not_found_returns_404(self, products_client: ProductsClient):
        with allure.step("Send DELETE request for non-existent product ID 999999"):
            response = products_client.delete_product(product_id=999999)
        
        with allure.step("Verify response status code is 404"):
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
