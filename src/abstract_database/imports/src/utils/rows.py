from .imports import *
def get_rows(rows):
    if not rows:
        return None
    if hasattr(rows, '_mapping'):          # single Row
        return dict(rows._mapping)
    if isinstance(rows, list):
        return [
            dict(row._mapping) if hasattr(row, '_mapping') else row
            for row in rows
        ]
    return rows


def get_last_row(table_name, **kwargs):
    db_name = kwargs.get('dbName', 'solcatcher')
    with get_engine(db_name).connect() as conn:
        result = conn.execute(
            text(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1;")
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
