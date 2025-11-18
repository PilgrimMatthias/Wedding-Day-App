import os


class Config:
    UPLOAD_PATH = os.path.join("static", "uploads")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
