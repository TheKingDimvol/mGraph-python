from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'neo4j+s://f16f555d.databases.neo4j.io'  # 'neo4j://176.57.217.75:7687'
    database_url_login: str = 'neo4j'
    database_url_password: str = 'taSRLYhUxPk-be012UMOmiV4T4ysl8trdYGvrwhMb9M'  # 'miner2'
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
