from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname : str 
    database_port: str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

# set up .env
# DATABASE_HOSTNAME = localhost
# DATABASE_PORT=5432
# DATABASE_PASSWORD=postgres
# DATABASE_NAME=fastapi
# DATABASE_USERNAME=postgres
# SECRET_KEY =12a26e3b2ffa1fdd14304ced9e550a2977167f72b165624b99ebd67d37bc4cb2
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=60

settings = Settings()
