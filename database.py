from typing import Optional

import databases
import pydantic

import ormar
import sqlalchemy

DATABASE_URL = "sqlite:///db.sqlite"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database

class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Users"

    id: int = ormar.Integer()
    username: int = ormar.String(max_length=100)
    is_anon: bool = ormar.Boolean(null=True)
    number: str = ormar.String(null=True)
    name: str = ormar.String(max_length=100)
    
    