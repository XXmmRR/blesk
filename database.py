from typing import Optional

import databases
import pydantic

import ormar
import sqlalchemy
from sqlalchemy.engine import create_engine

DATABASE_URL = "sqlite:///db.sqlite"

base_ormar_config = ormar.OrmarConfig(
    database=databases.Database(DATABASE_URL),
    metadata=sqlalchemy.MetaData(),
    engine=sqlalchemy.create_engine(DATABASE_URL),
)


class User(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="users")
    id: int = ormar.Integer(primary_key=True)
    tg_id: int = ormar.Integer()
    username: int = ormar.String(max_length=100)
    is_anon: bool = ormar.Boolean(nullable=True)
    number: str = ormar.String(nullable=True, max_length=100)
    name: str = ormar.String(max_length=100)
    
    
base_ormar_config.metadata.create_all(base_ormar_config.engine)