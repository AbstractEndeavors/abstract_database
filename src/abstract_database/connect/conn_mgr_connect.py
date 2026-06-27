from .imports import *
def get_conn_mgr():
    return connectionManager(
                  dbType='abstract_base',
                  dbName='admin')
def get_cur_conn(use_dict_cursor=True):
    """
    Get a database connection and a RealDictCursor.
    Returns:
        tuple: (cursor, connection)
    """
    conn = connectionManager().get_db_connection()
    cur = conn.cursor(row_factory=dict_row) if use_dict_cursor else conn.cursor()
    return cur, conn

def get_connection(env=None,env_path=None):
    """Establish a PostgreSQL connection."""
    env = dict(env or load_postgres_env(env_path))
    name_keys = ['dbname', 'dbName', 'database']
    dbname = None
    for key in name_keys:
        if key in env:
            dbname = env.pop(key)
    if dbname is not None:
        env['dbname'] = dbname
    env.pop('url', None)
    return psycopg.connect(**env)
