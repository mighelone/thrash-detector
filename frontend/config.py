class Config:
    DEBUG = False
    TESTING = False
    BACKEND_URL = ":8000"
    API_ENDPOINT = "/api/thrash/json"


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    BACKEND_URL = "http://localhost:28000"
    ENV = "development"


class ProductionConfig(Config):
    BACKEND_URL = "http://backend:8000"
