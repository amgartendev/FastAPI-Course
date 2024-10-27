from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "mysql+aiomysql://root:amgartendev@localhost:3306/faculdade"

    class Config:
        case_sensitive = True


settings: Settings = Settings()
