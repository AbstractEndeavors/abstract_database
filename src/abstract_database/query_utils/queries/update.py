from .imports import sql,build_return_clause,build_where_clause,build_set_clause
from .execute import execute_query
def update_any_combo(*,
                     table_name: str,
                     update_map: dict,
                     search_map: dict = None,
                     any_value: bool = False,
                     returning=False,        # False | True | 'count' | 'col1,col2'
                     zipit=True,
                     schema='public'):
    if not table_name or table_name == '*':
        raise ValueError("table_name is required")
    if not update_map:
        raise ValueError("update_map cannot be empty")
    search_map = search_map or {}
    base = sql.SQL("UPDATE {}.{} SET ").format(
        sql.Identifier(schema),
        sql.Identifier(table_name)
        )
    set_sql, values = build_set_clause(update_map)
    where_sql, values = build_where_clause(
        search_map,
        vals=values,
        any_value=any_value
        )
    return_sql = build_return_clause(returning=returning)
    qry = (
        base
        + set_sql
        + where_sql
        + return_sql
    )
    return execute_query(qry, values=values, zipRows=zipit)
