from .imports import *
def make_single(string):
  return string.replace('_','')
def make_multiple(string):
    nustring=''
    
    for char in string:
        if char in uppers:
            char = f"_{char.lower()}"
        nustring+=char
    return nustring
def get_table(method,tables):
  tableName = make_single(method.lower())
  table = [table for table in tables if table.get('tableName').lower() == tableName]
  if table and isinstance(table,list):
    table = table[0]
  return table
def get_db_vars(dbName, dbType=None,env_path=None):
    dbType='database'
    dbVars = {"user": None, "dbname": None, "host": None, "port": None, "password": None}
    for key in dbVars:
        env_key = f"{dbName.upper()}_{dbType.upper()}_{key.upper()}"
        dbVars[key] = get_env_value(key=env_key,path=get_env_path())
    return dbVars
def get_db_url(dbName, dbType=None):
    dbVars = get_db_vars(dbName, dbType=dbType)
    return f"postgresql://{dbVars['user']}:{dbVars['password']}@{dbVars['host']}:{dbVars['port']}/{dbVars['dbname']}"
def get_engine(dbName):
    db_url = get_db_url(dbName)
    engine = create_engine(db_url)
    return engine
