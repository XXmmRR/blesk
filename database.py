from typing import Optional

import databases
import pydantic

import ormar
import sqlalchemy

DATABASE_URL = "sqlite:///db.sqlite"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class User(ormar.Model):
    class Meta:
        metadata=metadata
        database=database
        tablename = "Users"

    id: int = ormar.Integer()
    username: int = ormar.String(max_length=100)
    is_anon: bool = ormar.Boolean(null=True)
    number: str = ormar.String(null=True)
    name: str = ormar.String(max_length=100)
    
metadata.create_all()