from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):

    DB_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_TIME_MINUTES:int
    REFRESH_TOKEN_TIME_DAYS:int
    ABS_DAY_LIFE:int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

settings = Settings()