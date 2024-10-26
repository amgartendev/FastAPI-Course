from pydantic_settings import BaseSettings
from typing import ClassVar
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "mysql+aiomysql://root:amgartendev@localhost:3306/faculdade"
    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
