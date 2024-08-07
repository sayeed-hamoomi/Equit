from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    database_username:str
    database_password:str
    database_host:str
    database_name:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    
    model_config = SettingsConfigDict(env_file='.env')


settings=Settings()