from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):

    DB_URL:str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

settings = Settings()