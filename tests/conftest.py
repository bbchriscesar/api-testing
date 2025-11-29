import pytest
import allure
from clients.products_client import ProductsClient


@pytest.fixture(scope="session")
def products_client():
    """Provides a shared ProductsClient instance for the test session."""
    with allure.step("Initialize Products API client"):
        client = ProductsClient()
    yield client
    with allure.step("Close Products API client"):
        client.close()


@pytest.fixture(scope="function")
def created_product(products_client):
    """Creates a test product and cleans it up after the test."""
    with allure.step("Create test product"):
        response = products_client.create_product(
            name="Test Product",
            price=99.99,
            description="Test product for automated testing",
            stock=10
        )
    
    if response.status_code == 201:
        product = response.json()
        allure.attach(
            str(product),
            name="Created Product",
            attachment_type=allure.attachment_type.JSON
        )
        yield product
        with allure.step(f"Cleanup: Delete product {product['id']}"):
            products_client.delete_product(product["id"])
    else:
        yield None
