import os


class Settings:
    BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    API_KEY = os.getenv("API_KEY", "NMI3Rvx-8WSUcQmhU_wEcWoRnEFOK55bKquPMy0l8bA")
    TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))


settings = Settings()
