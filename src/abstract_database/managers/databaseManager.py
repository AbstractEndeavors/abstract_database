from .imports import *
class DatabaseManager:
    def __init__(self, conn_mgr=None,**kwargs):
        self.conn_mgr = conn_mgr or connectionManager(**kwargs)
        self.connectionManager = self.conn_mgr
        self.dbname = self.conn_mgr.dbname
        self.user = self.conn_mgr.user
        self.password = self.conn_mgr.password
        self.host = self.conn_mgr.host
        self.port = self.conn_mgr.port
        self.table_config_path = get_env_value(key=f"{self.connectionManager.dbName.upper()}_{self.connectionManager.dbType.upper()}_CONFIGPATH", path=self.connectionManager.env_path)

    def connect_db(self):
        try:
            return psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg.OperationalError as e:
            print(f"Unable to connect to the database: {e}")
            sys.exit(1)

    def get_table_configuration(self, file_path=None):
        table_configuration_file_path = file_path or self.table_config_path
        try:
            if table_configuration_file_path and os.path.isfile(table_configuration_file_path):
                return safe_load_from_json(table_configuration_file_path)
        except Exception as e:
            print(f"No table config file path found: {e}")
        return []

    def get_dict_from_config(self, tableName, file_path=None):
        for config in self.get_table_configuration(file_path=file_path):
            if config.get('tableName').lower() == tableName.lower():
                return config

    def get_table_names(self, file_path=None):
        return [config.get('tableName') for config in self.get_table_configuration(file_path=file_path)]

    def get_first_row_as_dict(self, tableName, conn):
        query = f"SELECT * FROM {tableName} ORDER BY id ASC LIMIT 1;"
        conn = self.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            first_row = cur.fetchone()
            col_names = [desc[0] for desc in cur.description]
            if first_row:
                return dict(zip(col_names, first_row))
            return None
        except psycopg.Error as e:
            print(f"Error fetching the first row: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def analyze_variable_types(self, row):
        """Analyze the types of variables in a given row."""
        value_keys = {}
        if isinstance(row, dict):
            for key, value in row.items():
                value_keys[key] = str(type(value).__name__)  # Analyze types
        return value_keys

    def get_instruction_from_tableName(self, tableName=None):
        """Get instructions based on table configuration and data."""
        tableName = tableName or get_env_value(key="abstract_ai_table_name", path=self.env_path)
        table_samples = []
        table_samples.append({"DATABASE_CONFIG": self.get_dict_from_config(tableName), "explanation": "Database Table Configuration."})

        data = self.get_first_row_as_dict(tableName, self.connect_db())
        if data:
            table_samples.append({"ACTUAL_DATABASE_ROW": data, "explanation": f"First row of data from table {tableName} returned as a dictionary."})

            # Replace `get_value_keys` with the new type analysis function
            value_keys = self.analyze_variable_types(data)
            table_samples.append({"VALUE_KEYS": value_keys, "explanation": "Type Values for the Values in the Database SCHEMA."})

            table_samples.append({"AVAILABLE_FUNCTION_FOR_FILTERING": self.get_filtering_function(), "explanation": "Available function for filtering the database."})

        return table_samples

    def get_filtering_function(self):
        return """def search_multiple_fields(query):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg.Error as e:
        print(f"Error querying JSONB data: {e}")
    finally:
        cur.close()
        conn.close()
"""

    def search_multiple_fields(self,**kwargs):
        conn = self.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(**kwargs)
            return cur.fetchall()
        except psycopg.Error as e:
            print(f"Error querying JSONB data: {e}")
        finally:
            cur.close()
            conn.close()

    def save_to_excel(self, rows, file_path="output.xlsx"):
        excel_data = []
        if rows:
            for row in rows:
                row = list(row) if isinstance(row, tuple) else row
                excel_data.append(flatten_json(row, parent_key='', sep='_'))
            df = pd.DataFrame(excel_data)
            safe_excel_save(df, file_path)

    def get_query_save_to_excel(self, database_query, file_path="output.xlsx"):
        result = self.search_multiple_fields(**database_query)
        self.save_to_excel(result, file_path=file_path)
        return file_path
def ensure_db_manager(db_mgr=None, conn_mgr=None,**kwargs):
    return db_mgr or DatabaseManager(conn_mgr=conn_mgr,**kwargs)
