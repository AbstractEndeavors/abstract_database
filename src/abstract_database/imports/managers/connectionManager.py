from .imports import *
from .tableManager import *
from abstract_utilities import safe_split
ALIAS_KEYS = {
        "port": ["port"],
        "password": ["password", "pass"],
        "dbtype": ["type", "dbtype","dbType"],
        "host": ["host",  "address"],
        "user": ["user", "dbuser"],
        "dbname": ["dbname", "database", "name"],
        "env_path":["path","env_path","env"],
        "dburl":["url","dbUrl","dburl"]
    }
def get_safe_password(password):
    safe_password = quote_plus(password)
    return safe_password
# Existing utility functions remain the same
def get_dbType(dbType=None):
    return dbType or 'database'

def get_dbName(dbName=None):
    return dbName or 'abstract'

def get_dbUser(dbUser=None):
    return dbUser

def verify_env_path(env_path=None):
    return env_path or get_env_path()
def get_db_vars_from_kwargs(**kwargs):
    """
    Normalize DB-related kwargs into canonical connection variables.

    Accepted aliases (case-insensitive):
        port        -> port
        password    -> password, pass
        dbType      -> type, dbtype
        host        -> host, url, address
        dbUser      -> user, dbuser
        dbName      -> dbname, database, name
        env_path    -> path, env, env_path
    """
    resolved = {}

    

    # Normalize incoming kwargs once
    lowered_kwargs = {k.lower(): v for k, v in kwargs.items()}

    for canonical_key, aliases in ALIAS_KEYS.items():
        for alias in aliases:
            if alias in lowered_kwargs:
                resolved[canonical_key] = lowered_kwargs[alias]
                break  # stop searching aliases, not keys

    return resolved
def resolve_key(key_type):
    value = ALIAS_KEYS.get(key_type)
    if value:
        return key_type
    for key,values in ALIAS_KEYS.items():
        if key_type in values:
            return key
def resolve_values(key_type):
    values = ALIAS_KEYS.get(key_type)
    if values:
        return values
    for key,values in ALIAS_KEYS.items():
        if key_type in values:
            return values
def resolve_env_path(**kwargs):
    for key in ["path","env_path","env"]:
        env_path = kwargs.get(key)
        if env_path:
            return env_path
    return get_env_path()
def resolve_env_value(init_key,**kwargs):
    
    env_path = resolve_env_path(**kwargs)
    trukeys = {"env_path":env_path}
    for key,value in kwargs.items():
        tru_key = resolve_key(key)
        values = resolve_values(tru_key)
        for valu in values:
            nukey = f"{init_key}_{valu}".upper()
            env_value = get_env_value(nukey,env_path)
            if env_value:
               
                trukeys[key] = env_value
    return trukeys
def get_kwargs_dict(**kwargs):
    return kwargs
##def get_db_env_value(dbname,user,env_path=None,**kwargs):
##    env_path = verify_env_path(env_path)
##    dbname_part_key=""
##    user_part_key=""
##    if dbname:
##        dbname_part_key=f"{dbname}_"
##    if user:
##        user_part_key=f"{dbname_part_key}{user}_"
##    for key,value in kwargs.items():
##        value = get_env_value(value) or value
##        if not value:
##            for part_key in [dbname_part_key,user_part_key]:
##                temp_key = f"{part_key}{key}"
##                value = get_env_value(temp_key.upper(),path=env_path)
##                if value:
##                    break
##        kwargs[key]=value
##    return get_kwargs_dict(dbname=dbname,user=user,**kwargs)
def derive_partial_env_key(**kwargs):
    out_values = get_db_vars_from_kwargs(**kwargs)
    dbname = out_values.get("dbname")
    if dbname:
        data = read_from_file(get_env_path())
        data_lines = data.split('\n')
        for line in data_lines:
            line_spl = line.split('=')
            if len(line_spl) == 2:
                if eatAll(line_spl[-1],' ') == eatAll(dbname,' '):
                    key = eatAll(line_spl[0])
                    return '_'.join(key.split('_')[:-1])
    
def derive_env_key(key,**kwargs):
    partial_env_key = derive_partial_env_key(**kwargs)
    if partial_env_key:
        return f"{partial_env_key.upper()}_{key.upper()}"
def create_db_url(dict_obj=None,**kwargs):
    dict_obj = dict_obj or derive_db_vars(**kwargs)
    dburl = dict_obj.get('dburl') or dict_obj.get('url') or ""
    if dburl:
        return dburl
    dbtype = dict_obj.get('dbtype')
    dburl += f"{dbtype}://"
    user = dict_obj.get('user')
    dburl += f"{user}:"
    password = dict_obj.get('password')
    dburl += f"{password}@"
    host = dict_obj.get('host')
    dburl += f"{host}"
    port = dict_obj.get('port')
    dburl += f":{port}"
    dbname = dict_obj.get('dbname')
    dburl += f"/{dbname}"
    return dburl
    

def get_db_env_key(**kwargs):
    return get_db_env_value(**kwargs)
def derive_db_vars(**kwargs):
    db_vars = get_db_vars_from_kwargs(**kwargs)
    return get_db_env_key(**db_vars)
def get_db_vars(**kwargs):
    dbVars = derive_db_vars(**kwargs)
    dbVars['dburl'] = create_db_url(dict_obj=dbVars)
    return dbVars
def get_db_env_value(**kwargs):
    get_keys = ['dbtype','user','password','host','port','dbname','url']
    out_values = get_db_vars_from_kwargs(**kwargs)
    dbname = out_values.get("dbname")
    if dbname:
        dbname_part_key=f"{dbname}_".upper()
        for key in get_keys:
            env_value = out_values.get(key)
            if not env_value:
                env_key = f"{dbname_part_key}{key}".upper()
                env_value = get_env_value(env_key)
            if env_value:
                out_values[key] = env_value
    if 'url' in out_values:
        dbUrl = out_values.get("url")
        parts_from_db_url = get_parts_from_db_url(dbUrl)
        for key,value in out_values.items():
            if value == None:
                out_values[key] = parts_from_db_url.get(key)
        get_keys = [key for key in get_keys if out_values.get(key) == None]
    if 'dbtype' not in out_values or out_values.get('dbtype') == None:
        out_values['dbtype']='postgres'
        get_keys = [key for key in get_keys if key != 'dbtype']
    init_key = f"{out_values.get('dbname')}_{out_values.get('dbtype')}".upper()
    for key in get_keys:
        res_values = resolve_values(key)
        res_key = resolve_key(key)
        for value in res_values:
            values = resolve_env_value(init_key,**{value:None}).get(res_key)
            if values:
                out_values[res_key] = values
                break
    out_values['dburl'] = create_db_url(dict_obj=out_values) 
    return out_values
def get_parts_from_db_url(db_url):
    altered_url = db_url.replace('://','/').replace(':','/').replace('@','/')
    keys = ['dbtype','user','password','host','port','dbname']
    dbVars = {}
    for i,key in enumerate(keys):
        dbVars[key] = safe_split(altered_url,"/",i)
    return dbVars
logger = logging.getLogger(__name__)


class KeyedSingletonMeta(type):
    """Cache one instance per (class, connection-identity).

    Identity is derived from the connection-identifying kwargs (dbName,
    dbType, env_path, url). Calls with the same identity share an instance,
    and a no-argument call always maps to the same default instance -- this
    preserves the historic ``connectionManager()`` singleton behaviour while
    finally allowing several distinct databases to be managed at once.
    """
    _instances = {}

    def _identity(cls, *args, **kwargs):
        db = get_db_vars_from_kwargs(**kwargs)
        return (db.get('dbname'), db.get('dbtype'),
                db.get('env_path'), db.get('dburl'))

    def __call__(cls, *args, **kwargs):
        key = (cls, cls._identity(*args, **kwargs))
        inst = cls._instances.get(key)
        if inst is None:
            inst = super().__call__(*args, **kwargs)
            cls._instances[key] = inst
        return inst


class connectionManager(metaclass=KeyedSingletonMeta):

    def __init__(self, tables=None, tables_path=None, **kwargs):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self.dbVars = get_db_env_value(**kwargs)

        self.dbUrl = self.dburl = self.dbVars.get('dburl')
        self.env_path = self.dbVars.get('env_path')
        self.dbType = self.dbVars.get('dbtype')
        self.dbName = self.dbname = self.dbVars.get('dbname')
        self.dbUser = self.user = self.dbVars.get('user')
        self.dbVars = self.get_db_vars(**self.dbVars)
        self.password = self.dbVars.get('password')
        self.host = self.dbVars.get('host')
        self.port = self.dbVars.get('port')

        self.table_mgr = TableManager()
        self.table_mgr.env_path = self.env_path
        self.tables = tables or (safe_load_from_json(file_path=tables_path)
                                 if tables_path else None) or []
        # Connections are opened lazily on first use. Constructing a manager
        # must never touch the database -- doing so historically blocked
        # imports and app startup whenever the DB was unreachable.
        self._inserts_ready = False

    def ensure_inserts(self):
        """Create configured tables / load the insert list once, on demand.

        Safe to call repeatedly. A connection or setup failure is logged
        rather than silently swallowed, but does not raise, so the common
        table-less caller is unaffected.
        """
        if self._inserts_ready:
            return True
        if self.tables:
            try:
                self.table_mgr.add_insert_list(
                    self.tables, self.dbName, self.connect_db())
            except Exception as e:
                logger.warning(
                    "Could not initialize tables for db '%s': %s",
                    self.dbName, e)
                return False
        self._inserts_ready = True
        return True

    # Backwards-compatible alias for the old eager hook.
    def check_conn(self):
        return self.ensure_inserts()

    def get_dbName(self, dbName=None):
        return get_dbName(dbName=dbName or self.dbName)
    def get_dbType(self, dbType=None):
        return get_dbType(dbType=dbType or self.dbType)
    def get_dbUser(self, dbUser=None):
        return get_dbUser(dbUser=dbUser or self.dbUser)
    def get_env_path(self, env_path=None):
        return verify_env_path(env_path=env_path)

    def get_db_vars(self,**kwargs):
        return get_db_vars(**kwargs)

    def change_db_vars(self, tables=None, tables_path=None, **kwargs):
        """Re-resolve this manager's connection settings in place.

        Resets the lazy state so the next call reconnects with the new
        settings; it does not open a connection itself.
        """
        self.dbVars = self.get_db_vars(**derive_db_vars(**kwargs))
        self.dbUrl = self.dburl = self.dbVars.get('dburl')
        self.env_path = self.dbVars.get('env_path')
        self.dbType = self.dbVars.get('dbtype')
        self.dbName = self.dbname = self.dbVars.get('dbname')
        self.dbUser = self.user = self.dbVars.get('user')
        self.password = self.dbVars.get('password')
        self.host = self.dbVars.get('host')
        self.port = self.dbVars.get('port')
        if tables or tables_path:
            self.tables = tables or safe_load_from_json(file_path=tables_path) or []
        self.table_mgr.env_path = self.env_path
        self._inserts_ready = False
        return self.dbVars

    def connect_db(self):
        """Open and return a new database connection.

        Priority: resolved ``dburl`` first, then individual connection
        parameters. Raises ``ConnectionError`` (with the underlying cause)
        if neither works, so failures surface immediately instead of
        returning ``None`` and breaking downstream with a vague error.
        """
        errors = []
        if self.dbUrl:
            try:
                return psycopg.connect(self.dbUrl)
            except Exception as e:
                errors.append(f"url: {e}")
        if self.host and self.dbname:
            try:
                return psycopg.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    dbname=self.dbname,
                )
            except Exception as e:
                errors.append(f"params: {e}")
        raise ConnectionError(
            f"Unable to connect to database '{self.dbName}'. "
            + (f"Tried -> {'; '.join(errors)}." if errors
               else "No usable connection settings were found.")
        )

    def simple_connect_db(self):
        """ Create a connection pool using the database URL """
        if self.dburl:
            return ConnectionPool(1, 10, self.dburl)
        else:
            return ConnectionPool(1, 10, user=self.user,
                                                      password=self.password,
                                                      host=self.host,
                                                      port=self.port,
                                                      database=self.dbname)

    def put_db_connection(self, conn=None):
        """Close a connection. Connections are opened per call, so there is
        no pool to return to -- this simply closes the handle."""
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                logger.debug("put_db_connection: error closing connection: %s", e)

    def get_db_connection(self):
        return self.connect_db()

    def get_insert(self, tableName):
        self.ensure_inserts()
        return self.table_mgr.get_insert(tableName)

    def fetchFromDb(self, tableName, searchValue):
        self.ensure_inserts()
        return self.table_mgr.fetchFromDb(tableName, searchValue, self.connect_db())

    def insertIntoDb(self, tableName, searchValue, insertValue):
        self.ensure_inserts()
        return self.table_mgr.insert_intoDb(tableName, searchValue, insertValue, self.connect_db())

    def search_multiple_fields(self, query, **kwargs):
        return self.table_mgr.search_multiple_fields(query=query, conn=self.connect_db())

    def get_first_row_as_dict(self, tableName=None, rowNum=1):
        return self.table_mgr.get_first_row_as_dict(tableName=tableName, rowNum=rowNum, conn=self.connect_db())
def create_connection(**kwargs):
    return connectionManager(**kwargs)

def get_db_connection(**kwargs):

    return connectionManager(**kwargs).get_db_connection()

def put_db_connection(conn):
    connectionManager().put_db_connection(conn)

def connect_db(**kwargs):
    return connectionManager(**kwargs).connect_db()

def get_insert(tableName,**kwargs):
    return connectionManager(**kwargs).get_insert(tableName)

def fetchFromDb(tableName, searchValue,**kwargs):
    return connectionManager(**kwargs).fetchFromDb(tableName, searchValue)

def insertIntoDb(tableName, searchValue, insertValue,**kwargs):
    return connectionManager(**kwargs).insertIntoDb(tableName, searchValue, insertValue)

def search_multiple_fields(query, **kwargs):
    return connectionManager().search_multiple_fields(query, **kwargs)

def get_first_row_as_dict(tableName=None, rowNum=1):
    return connectionManager().get_first_row_as_dict(tableName, rowNum)
def get_cur_conn(use_dict_cursor=True):
    """
    Get a database connection and a RealDictCursor.
    Returns:
        tuple: (cursor, connection)
    """
    conn = connectionManager().get_db_connection()
    cur = conn.cursor(row_factory=dict_row) if use_dict_cursor else conn.cursor()
    return cur, conn
