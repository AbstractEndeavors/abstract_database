from .imports import sql,build_return_clause,build_where_clause
def select_all(query: str, *args):
    """
    Execute a SELECT query that returns zero or more rows.
    Returns:
        list[dict]: list of rows, empty if none.
    """
    cur, conn = get_cur_conn()
    try:
        cur.execute(query, args) if args else cur.execute(query)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()
def select_distinct_rows(query: str, *args):
    """
    Execute a SELECT query that returns zero or more rows.
    Returns:
        list[dict]: a list of RealDictCursor rows (dicts), empty if none.
    """
    cur, conn = get_cur_conn()
    try:
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()
def select_rows(query: str, *args):
    """
    Execute a SELECT query that returns a single row or None.
    Args:
        query (str): The SQL query with %s placeholders.
        *args: Parameters to substitute into the query.
    Returns:
        A dictionary if a row is found, else None.
    """
##    print("DEBUG select_rows—type(query):", type(query), " value:", query)
    cur, conn = get_cur_conn()
    try:
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        row = cur.fetchone()
        return row or []
    finally:
        cur.close()
        conn.close()




