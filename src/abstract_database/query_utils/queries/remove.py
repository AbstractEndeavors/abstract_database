from .imports import sql,build_return_clause,build_where_clause
from .execute import execute_query
def remove_any_combo(*,
                    column_names='*',
                    table_name,
                    search_map=None,
                    count=False,
                    any_value=False,
                    returning=False,        # False | True | 'count' | 'col1,col2'
                    zipit=True,
                    schema='public'):
    """
    Delete records from a specified table with optional filtering.

    Args:
        table_name (str): Name of the table to delete from.
        search_map (dict, optional): Dictionary of column-value pairs for WHERE clause.
        any_value (bool): If True, uses ANY() in WHERE clause for array values.
        returning (False | True | 'count' | str): Specifies return behavior.
            - False: No return.
            - True: Return all columns.
            - 'count': Return count of deleted rows.
            - str: Comma-separated column names to return.
        zipit (bool): If True, zips rows into a more compact format.
        schema (str): Database schema name (default: 'public').

    Returns:
        List of results from query_data, format depends on returning and zipit.

    Raises:
        ValueError: If table_name is invalid or missing.
    """
    if not table_name or table_name == '*':
        raise ValueError("table_name is required")
    search_map = search_map or {}
    
    base = sql.SQL("DELETE FROM {}.{}").format(
        sql.Identifier(schema),
        sql.Identifier(table_name)
    )
    
    where_sql, values = build_where_clause(
        search_map,
        any_value=any_value
    )
    
    return_sql = build_return_clause(returning=returning)
    
    qry = (
        base
        + where_sql
        + return_sql
    )
    
    return execute_query(qry, values=values, zipRows=zipit)
