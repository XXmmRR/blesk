from typing import Optional

import databases
import pydantic

import ormar
import sqlalchemy
from sqlalchemy.engine import create_engine

DATABASE_URL = "sqlite:///db.sqlite"
metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
    
    
class User(ormar.Model):
    class Meta(MainMeta):
        tablename = "Users"

    id: int = ormar.Integer()
    username: int = ormar.String(max_length=100)
    is_anon: bool = ormar.Boolean(nullable=True)
    number: str = ormar.String(nullable=True, max_length=100)
    name: str = ormar.String(max_length=100)
    
    
metadata.create_all(engine)