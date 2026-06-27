import logging,os,yaml,io,requests,time,json,warnings,traceback,asyncio
from abstract_essentials import lazy_module
# heavy/compiled deps deferred to first use via lazy_module — kept off the import path
pd = lazy_module("pandas")
np = lazy_module("numpy")
psycopg = lazy_module("psycopg")
asyncpg = lazy_module("asyncpg")
Image = lazy_module("PIL.Image")
from datetime import datetime, timedelta
from typing import *
logging.basicConfig()

