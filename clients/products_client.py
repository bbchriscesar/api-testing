import requests
from typing import Optional
from clients.base_client import BaseClient


class ProductsClient(BaseClient):
    
    ENDPOINT = "/products/"
    
    def get_products(self, skip: int = 0, limit: int = 100) -> requests.Response:
        params = {"skip": skip, "limit": limit}
        return self.get(self.ENDPOINT, params=params)
    
    def get_product(self, product_id: int) -> requests.Response:
        endpoint = f"{self.ENDPOINT}{product_id}"
        return self.get(endpoint)
    
    def create_product(self, name: str, price: float, description: Optional[str] = None, 
                       stock: int = 0) -> requests.Response:
        payload = {
            "name": name,
            "price": price,
            "stock": stock
        }
        if description:
            payload["description"] = description
        
        return self.post(self.ENDPOINT, data=payload)
    
    def update_product(self, product_id: int, **kwargs) -> requests.Response:
        endpoint = f"{self.ENDPOINT}{product_id}"
        return self.patch(endpoint, data=kwargs)
    
    def delete_product(self, product_id: int) -> requests.Response:
        endpoint = f"{self.ENDPOINT}{product_id}"
        return self.delete(endpoint)
