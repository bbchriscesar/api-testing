import pytest
import allure
from clients.products_client import ProductsClient


@allure.epic("Products API")
@allure.feature("POST Products")
class TestCreateProduct:

    @allure.story("Create Product")
    @allure.title("Create product with valid data returns 201 Created")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_product_returns_201(self, products_client: ProductsClient):
        with allure.step("Prepare product payload"):
            payload = {
                "name": "Test Product",
                "price": 99.99,
                "description": "Test product for automated testing",
                "stock": 10
            }
            allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Send POST request to create product"):
            response = products_client.create_product(
                name=payload["name"],
                price=payload["price"],
                description=payload["description"],
                stock=payload["stock"]
            )
        
        with allure.step("Verify response status code is 201"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        with allure.step("Verify response body contains correct data"):
            response_data = response.json()
            allure.attach(str(response_data), name="Response Body", attachment_type=allure.attachment_type.JSON)
            assert response_data["name"] == "Test Product"
            assert response_data["price"] == 99.99
            assert response_data["description"] == "Test product for automated testing"
            assert response_data["stock"] == 10
            assert "id" in response_data
        
        with allure.step("Cleanup: Delete created product"):
            products_client.delete_product(response_data["id"])

    @allure.story("Validation")
    @allure.title("Create product without required fields returns 422")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_product_without_required_fields_returns_422(self, products_client: ProductsClient):
        with allure.step("Send POST request with empty payload"):
            response = products_client.post("/products/", data={})
        
        with allure.step("Verify response status code is 422"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    @allure.story("Validation")
    @allure.title("Create product with invalid price type returns 422")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_product_with_invalid_price_returns_422(self, products_client: ProductsClient):
        with allure.step("Send POST request with invalid price type"):
            response = products_client.post("/products/", data={
                "name": "Invalid Product",
                "price": "invalid_price",
                "stock": 10
            })
        
        with allure.step("Verify response status code is 422"):
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    @allure.story("Validation")
    @allure.title("Create product with negative price")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_create_product_with_negative_price_returns_200(self, products_client: ProductsClient):
        with allure.step("Send POST request with negative price"):
            response = products_client.create_product(
                name="Negative Price Product",
                price=-10.00,
                stock=5
            )
        
        with allure.step("Verify response and cleanup if needed"):
            if response.status_code == 200:
                response_data = response.json()
                products_client.delete_product(response_data["id"])
        
        with allure.step("Verify response status code is 200 or 422"):
            assert response.status_code in [200, 422], f"Expected 200 or 422, got {response.status_code}"
