from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_KEY: str 
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str

    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_DB: int
    
    BROKER_USER: str
    BROKER_PASS: str
    BROKER_PORT: int
    BROKER_HOST: str
    
    model_config = SettingsConfigDict(env_file = '../.env')
    
    @property
    def database_url(self):
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    

settings = Settings()