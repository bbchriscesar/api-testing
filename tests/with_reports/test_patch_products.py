import pytest
import allure
from clients.products_client import ProductsClient


@allure.epic("Products API")
@allure.feature("PATCH Products")
class TestUpdateProduct:

    @allure.story("Update Product")
    @allure.title("Update product with valid data returns 200 OK")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_update_product_returns_200(self, products_client: ProductsClient, created_product):
        if created_product is None:
            pytest.skip("Product creation failed")
        
        with allure.step("Prepare update payload"):
            update_data = {"name": "Updated Product Name", "price": 149.99}
            allure.attach(str(update_data), name="Update Payload", attachment_type=allure.attachment_type.JSON)
        
        with allure.step(f"Send PATCH request to update product {created_product['id']}"):
            response = products_client.update_product(
                product_id=created_product["id"],
                name="Updated Product Name",
                price=149.99
            )
        
        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        with allure.step("Verify response body contains updated data"):
            response_data = response.json()
            allure.attach(str(response_data), name="Response Body", attachment_type=allure.attachment_type.JSON)
            assert response_data["name"] == "Updated Product Name"
            assert response_data["price"] == 149.99

    @allure.story("Update Product")
    @allure.title("Update non-existent product returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_update_product_not_found_returns_404(self, products_client: ProductsClient):
        with allure.step("Send PATCH request for non-existent product ID 999999"):
            response = products_client.update_product(
                product_id=999999,
                name="Non-existent Product"
            )
        
        with allure.step("Verify response status code is 404"):
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    @allure.story("Validation")
    @allure.title("Update product with invalid data returns 422")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_update_product_with_invalid_data_returns_422(self, products_client: ProductsClient, created_product):
        if created_product is None:
            pytest.skip("Product creation failed")
        
        with allure.step(f"Send PATCH request with invalid price type for product {created_product['id']}"):
            response = products_client.patch(f"/products/{created_product['id']}", data={
                "price": "invalid_price"
            })
        
        with allure.step("Verify response status code is 422"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"
