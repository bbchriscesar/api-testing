import requests
from typing import Optional
from config.settings import settings


class BaseClient:
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or settings.BASE_URL
        self.api_key = api_key or settings.API_KEY
        self.timeout = settings.TIMEOUT
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"
    
    def get(self, endpoint: str, params: Optional[dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, timeout=self.timeout, **kwargs)
    
    def post(self, endpoint: str, data: Optional[dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.post(url, json=data, timeout=self.timeout, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.patch(url, json=data, timeout=self.timeout, **kwargs)
    
    def put(self, endpoint: str, data: Optional[dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.put(url, json=data, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        return self.session.delete(url, timeout=self.timeout, **kwargs)
    
    def close(self):
        self.session.close()
