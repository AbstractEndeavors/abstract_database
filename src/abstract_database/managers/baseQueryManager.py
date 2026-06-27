from ..imports import *

class BaseQueryManager(metaclass=SingletonMeta):
    """
    Generic query manager: load <basename>.json for named queries,
    provide generic insert/update helpers, plus run() for custom SQL.
    """
    def __init__(self, basename: str, logs_on: bool = True):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        self.logs_on = logs_on
        self.toggle_trigger = {True: False, False: True}

        # load your JSON / YAML for this manager
        data = get_yaml_queries_data(basename)
        self._queries = data

        # dynamically set self._query_<key> = the SQL string
        for key, sql in data.items():
            setattr(self, f"_query_{key}", sql)
    def display_query_options(self) -> None:
        for key,value in self._queries.items():
            print(f"{key}:\n{value}\n\n")
    def toggle_logs(self, toggle: Optional[bool] = None) -> None:
        self.logs_on = not self.logs_on if toggle is None else bool(toggle)

    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generic INSERT: builds SQL from data dict, returns inserted row.
        """
        cols = list(data.keys())
        vals = [data[c] for c in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        col_list = ", ".join(cols)
        sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) RETURNING *;"
        return select_one(sql, *vals)

    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generic UPDATE: set columns from data dict, filter by where dict, returns updated row.
        """
        set_cols = list(data.keys())
        set_expr = ", ".join([f"{col} = %s" for col in set_cols])
        set_vals = [data[c] for c in set_cols]

        where_cols = list(where.keys())
        where_expr = " AND ".join([f"{col} = %s" for col in where_cols])
        where_vals = [where[c] for c in where_cols]

        sql = f"UPDATE {table} SET {set_expr} WHERE {where_expr} RETURNING *;"
        return select_one(sql, *(set_vals + where_vals))

    def run(
        self,
        key: str,
        *args,
        one: bool = False,
        many: bool = False,
        commit: bool = False,
        returning: bool = False,
        map_fn: Optional[Any] = None,
    ) -> Any:
        """
        Execute a query by its key from the loaded YAML/JSON.
        """
        sql = self._queries.get(key)
        if not sql:
            raise KeyError(f"Query '{key}' not found in configuration.")

        if self.logs_on:
            initialize_call_log()

        if many:
            rows = select_distinct_rows(sql, *args)
            return map_fn(rows) if map_fn else rows

        if one:
            row = select_rows(sql, *args)
            return map_fn(row) if (map_fn and row) else row

        if returning:
            return insert_query(sql, *args)

        if commit:
            execute_query(sql, *args)
            return None

        return select_distinct_rows(sql, *args)
