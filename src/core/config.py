import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")


class DBSettings(BaseSettings):
    port: int = os.environ.get("DB_PORT")
    host: str = os.environ.get("DB_HOST")
    db_user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASS")
    name: str = os.environ.get("DB_NAME")
    test_name: str = os.environ.get("TEST_DB_NAME")
    test_port: int = os.environ.get("DB_TEST_PORT")
    test_host: str = os.environ.get("DB_HOST")
    test_db_user: str = os.environ.get("DB_TEST_USER")
    test_db_password: str = os.environ.get("DB_TEST_PASS")


class Settings:
    db: DBSettings = DBSettings()


settings = Settings()
