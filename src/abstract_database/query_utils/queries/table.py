from .imports import *
from .execute import *
def get_all_table_names(schema='public'):
    """Fetch all table names from a specified schema."""
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE';
    """
    results = execute_query(query, values=(schema,), fetch=True, zipIt=True)
    rows = get_rows(results)
    return [row[0] for row in rows]
def get_table_info(table_name,schema='public'):
    """Fetch all table names from a specified schema."""
    query = """f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1;"""
    results = execute_query(query)
    rows = get_rows(results)
    return rows
def print_all_tables(queries):
    for key,value in queries.items():
        print(f"{key}: {value}\n\n")
