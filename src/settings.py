from dataclasses import dataclass
from os import environ

import dotenv


@dataclass
class Settings:
    MSSQL_SERVER: str
    MSSQL_PORT: int
    MSSQL_DATABASE: str
    MSSQL_USERNAME: str
    MSSQL_PASSWORD: str


dotenv.load_dotenv(
    dotenv_path=".env",
    override=False,
)

settings = Settings(
    MSSQL_SERVER=environ["MSSQL_SERVER"],
    MSSQL_PORT=int(environ["MSSQL_PORT"]),
    MSSQL_DATABASE=environ["MSSQL_DATABASE"],
    MSSQL_USERNAME=environ["MSSQL_USERNAME"],
    MSSQL_PASSWORD=environ["MSSQL_PASSWORD"],
)
