class Config:
    DEBUG = False
    TESTING = False
    BACKEND_URL = ":8000"


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    BACKEND_URL = "http://localhost:8000"
    ENV = "development"


class ProductionConfig(Config):
    BACKEND_URL = "http://backend:8000"
