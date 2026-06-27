from abstract_essentials import lazy_module
# psycopg (compiled DB driver) deferred to first use; SQLAlchemy ORM stays eager (the backbone).
psycopg = lazy_module("psycopg")
sql = lazy_module("psycopg.sql")          # used as sql.SQL(...) / sql.Identifier(...)

def Json(*args, **kwargs):                # used as Json(value)
    from psycopg.types.json import Jsonb
    return Jsonb(*args, **kwargs)

def connect(*args, **kwargs):             # bare connect() if any caller uses it
    import psycopg as _pg
    return _pg.connect(*args, **kwargs)

def dict_row(cursor):                     # row_factory=dict_row — psycopg is loaded by cursor time
    from psycopg.rows import dict_row as _dr
    return _dr(cursor)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import text,Boolean, create_engine, String, BigInteger, JSON, Text, cast, Index, MetaData, Table, text, inspect, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
