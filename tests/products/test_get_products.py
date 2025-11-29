import pytest
import allure
from clients.products_client import ProductsClient


@allure.epic("Products API")
@allure.feature("GET Products")
class TestGetProducts:

    @allure.story("List Products")
    @allure.title("Get all products returns 200 OK")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_get_products_returns_200(self, products_client: ProductsClient):
        with allure.step("Send GET request to /products/"):
            response = products_client.get_products()
        
        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        with allure.step("Verify response is a list"):
            response_data = response.json()
            allure.attach(
                str(response_data),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            assert isinstance(response_data, list), "Response should be a list of products"

    @allure.story("Authentication")
    @allure.title("Get products without API key returns 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_products_without_api_key_returns_200(self):
        with allure.step("Create client without API key"):
            client = ProductsClient(api_key="")
        
        with allure.step("Send GET request to /products/"):
            response = client.get_products()
        
        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        client.close()

    @allure.story("Authentication")
    @allure.title("Get products with invalid API key returns 403 Forbidden")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_get_products_with_invalid_api_key_returns_403(self):
        with allure.step("Create client with invalid API key"):
            client = ProductsClient(api_key="invalid-api-key-12345")
        
        with allure.step("Send GET request to /products/"):
            response = client.get_products()
        
        with allure.step("Verify response status code is 403"):
            assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        
        client.close()

    @allure.story("Get Single Product")
    @allure.title("Get non-existent product returns 404 Not Found")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_product_not_found_returns_404(self, products_client: ProductsClient):
        with allure.step("Send GET request for non-existent product ID 999999"):
            response = products_client.get_product(product_id=999999)
        
        with allure.step("Verify response status code is 404"):
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
