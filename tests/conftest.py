import pytest
from clients.products_client import ProductsClient


@pytest.fixture(scope="session")
def products_client():
    client = ProductsClient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def created_product(products_client):
    response = products_client.create_product(
        name="Test Product",
        price=99.99,
        description="Test product for automated testing",
        stock=10
    )
    
    if response.status_code == 201:
        product = response.json()
        yield product
        products_client.delete_product(product["id"])
    else:
        yield None
