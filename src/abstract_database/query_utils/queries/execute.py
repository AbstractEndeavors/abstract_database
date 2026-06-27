from .imports import *

def Json(*args, **kwargs):                # deferred: psycopg loads on first coercion call
    from psycopg.types.json import Json as _J
    return _J(*args, **kwargs)

_COERCE_REGISTRY: dict[type, callable] = {
    dict: Json,
    list: Json,
}

def _coerce_value(v):
    coercer = _COERCE_REGISTRY.get(type(v))
    return coercer(v) if coercer else v

def _coerce_values(values):
    if values is None:
        return None
    return [_coerce_value(v) for v in values]
def execute_query(query, values=None, fetch=True,**kwargs):
    """
    Execute a SQL query and return results if applicable.
    
    Args:
        query (str or psycopg.sql.Composed): SQL query to execute.
        values (tuple, optional): Values for parameterized queries.
        fetch (bool): Whether to fetch results (for SELECT) or commit (for INSERT/UPDATE).
        as_dict (bool): Return results as dictionaries if True, else as tuples.
    
    Returns:
        list: Query results (empty if no fetch or error).
    """
    row_factory = dict_row if resolve_as_dict(**kwargs) else None
    cur,conn = get_cur_conn(row_factory)

    # Convert Composed query to string if necessary
    if isinstance(query, sql.Composed):
        query_str = query.as_string(conn)
    else:
        query_str = str(query)

    logger.info(f"Executing query: {query_str} with values: {values}")

    
    try:
        with conn.cursor(row_factory=row_factory) as cursor:
            cursor.execute(query_str, _coerce_values(values))
            if fetch and query_str.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                if result:
                    logger.debug(f"First row: {result[0]}")
                return result
            conn.commit()
            return []
    except Exception as e:
        conn.rollback()
        logger.error(f"Query failed: {query_str}\nValues: {values}\nError: {e}\n{traceback.format_exc()}")
        return []
    finally:
        conn.close()
