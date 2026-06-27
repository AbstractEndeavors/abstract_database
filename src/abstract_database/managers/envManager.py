from .imports import *
def get_db_key(dbName, dbType, extra=None):
    key = f"{dbName.upper()}_{dbType.upper()}"
    if extra:
        key += f"_{extra.upper()}"
    return key

def get_bot_name():
    return 'darnell'

def get_pure_env_value(key=None, path=None):
    return get_env_value(path=path or get_env_path(), key=key)

def get_bot_env_key(key):
    return get_env_value(path=get_env_path(), key=f"{get_bot_name()}_{key}")

def get_env_key(key, path=None):
    return get_pure_env_value(path=path or get_env_path(), key=key)

def get_open_ai_key():
    return get_env_key('open_ai')

def get_discord_token():
    return get_env_key('token')

def get_application_id():
    return get_env_key('application_id')

def get_client_id():
    return get_env_key('client_id')

def get_client_secret():
    return get_env_key('client_secret')

def get_public_key():
    return get_env_key('public_key')

def get_dbType(dbType=None):
    return f"_{dbType}" if dbType else ''

def create_insert_list_file(dbName, dbType=None):
    return f"{dbName}{get_dbType(dbType)}_table_config.json"

def get_table_from_tables(dbName,tables=None):
  dbName_lower = str(dbName).lower()
  tables = tables or get_insert_list(dbName)
  
  for table in tables:
    if dbName_lower in table.get('tableName').lower():
        return table
class envManager(metaclass=SingletonMeta):
    def __init__(self, tables_dir=None, env_path=None, dbType=None,
                 insert_list_file=None):
        if not hasattr(self, 'initialized'):
          self.initialized = True
          # Configuration is environment-driven so the package is portable
          # across machines. Previously these were hardcoded to a developer's
          # personal Desktop path, which broke every other deployment.
          self.tables_dir = tables_dir or os.environ.get('ABSTRACT_DB_TABLES_DIR')
          self.env_path = env_path or os.environ.get('ABSTRACT_DB_ENV_PATH')
          self.dbType = dbType or os.environ.get('ABSTRACT_DB_TYPE', 'database')
          self.insert_list_file = insert_list_file or os.environ.get('ABSTRACT_DB_INSERT_LIST_FILE')
          self.insert_list_path = (
              os.path.join(self.tables_dir, self.insert_list_file)
              if self.tables_dir and self.insert_list_file else None)
          self.repo = {}
          self.initialized = True
    
    def var_check(self, dbName, dbType=None):
        dbType = dbType or self.dbType
        if dbName not in self.repo:
            self.repo[dbName] = {}
        if dbType not in self.repo[dbName]:
            self.repo[dbName][dbType] = {
                "env_path": self.env_path,
                "tables_dir": self.tables_dir,
                "insert_list_file": self.insert_list_file,
                "insert_list_path": self.insert_list_path
            }

    def add_to_memory(self, dbName, dbType=None, env_path=None, tables_dir=None, insert_list_file=None,insert_list_path=None,tables=None,table=None):
        dbType = dbType or self.dbType
        self.var_check(dbName, dbType=dbType)
        env_path = env_path or self.repo[dbName][dbType]["env_path"]
        tables_dir = tables_dir or self.repo[dbName][dbType]["tables_dir"]
        
        insert_list_file = insert_list_file or create_insert_list_file(dbName, dbType=dbType)
        insert_list_path = insert_list_path or os.path.join(tables_dir, insert_list_file)
        
        dbVars = self.get_db_vars(dbName, dbType=dbType, env_path=env_path)
        if insert_list_path and os.path.isfile(insert_list_path):
            tables = tables or safe_load_from_json(insert_list_path)
        table = table or get_table_from_tables(dbName,tables)
        self.repo[dbName][dbType] = {
            "env_path": env_path,
            "tables_dir": tables_dir,
            "dbVars": dbVars,
            "insert_list_file": insert_list_file,
            "insert_list_path": insert_list_path,
            "tables": tables,
            "table":table,
            "conn_mgr": self.get_conn_mgr(dbName=dbName, dbType=dbType, env_path=env_path, tables=tables, dbVars=dbVars)
        }

    def get_from_memory(self, dbName, dbType=None, variable=None):
        dbType = dbType or self.dbType
        self.var_check(dbName, dbType=dbType)
        return self.repo[dbName][dbType].get(variable, self.repo[dbName][dbType])

    def get_db_url(self, dbName, dbType=None, dbVars=None, env_path=None):
        dbType = dbType or self.dbType
        protocol = 'postgresql' if 'rabbit' not in dbType.lower() else 'amqp'
        dbVars = dbVars or self.get_db_vars(dbName=dbName, dbType=dbType, env_path=env_path)
        dbVars['dburl'] = f"{protocol}://{dbVars['user']}:{dbVars['password']}@{dbVars['host']}:{dbVars['port']}/{dbVars['dbname']}"
        return dbVars

    def get_db_vars(self, dbName, dbType=None, env_path=None):
        dbType = dbType or self.dbType
        env_path = env_path or self.get_from_memory(dbName, dbType=dbType, variable="env_path")
        dbVars = {"user": None, "dbname": None, "host": None, "port": None, "password": None}
        for key in dbVars:
            dbVars[key] = get_pure_env_value(key=get_db_key(dbName, dbType, key), path=env_path)
        return self.get_db_url(dbName=dbName, dbType=dbType, dbVars=dbVars, env_path=env_path)

    def get_conn_mgr(self, dbName, dbType=None, env_path=None, tables=None, dbVars=None):
        dbType = dbType or self.dbType
        env_path = env_path or self.get_from_memory(dbName, dbType=dbType, variable="env_path")
        tables = tables or get_insert_list(dbName, dbType=dbType)
        dbVars = dbVars or self.get_db_vars(dbName=dbName, dbType=dbType, env_path=env_path)
        return connectionManager(dbName=dbName, dbType=dbType, env_path=env_path, tables=tables, dbVars=dbVars)

def get_table(dbName, dbType=None):
    return envManager().get_from_memory(dbName, dbType=dbType, variable="table")

def get_tables_dir(dbName, dbType=None):
    return envManager().get_from_memory(dbName, dbType=dbType, variable="tables_dir")

def get_env_path(dbName, dbType=None):
    return envManager().get_from_memory(dbName, dbType=dbType, variable="env_path")

def get_insert_list_path(dbName, dbType=None):
    return envManager().get_from_memory(dbName, dbType=dbType, variable="insert_list_path")

def get_conn_mgr(dbName, dbType=None, env_path=None, tables=None):
    return envManager().get_from_memory(dbName, dbType=dbType, variable="conn_mgr")

def get_insert_list(dbName, dbType=None):
    return envManager().get_from_memory(dbName=dbName, dbType=dbType,variable="tables")

def getInsertType(tableName=None, table_configurations=None, dbName=None, dbType=None):
    table_configurations = table_configurations or get_insert_list(dbName=dbName, dbType=dbType)
    insertList = [ls for ls in table_configurations if ls.get("tableName").lower() == tableName.lower()]
    return insertList[0] if insertList else None

def dump_if_dict(obj):
    return json.dumps(obj) if isinstance(obj, dict) else obj

