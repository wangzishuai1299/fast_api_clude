from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str="mysql+pymysql://root:root@127.0.0.1:3306/fastapi_day02_page?charset=utf8mb4"
    APP_TITLE: str="书籍管理系统"
settings = Settings()