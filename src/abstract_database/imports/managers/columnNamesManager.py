from .imports import *
from .tableManager import *
from .connectionManager import *
class columnNamesManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):  
            self.initialized = True
            self.columnNames = {}

    def get_column_names(self, tableName, schema='public'):
        if tableName not in self.columnNames:
            self.columnNames[tableName] = self.fetch_column_names(tableName, schema)
        return self.columnNames[tableName]

    def fetch_column_names(self, tableName, schema='public'):
        query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = %s
            ORDER BY ordinal_position;
        """
        cur,conn = get_cur_conn()
                     
        results = fetch_data(query, [tableName, schema],conn,cur)
        if results:
            names = []
            for key,value in results.items():
                names.append(value)
            return names
        logger.warning(f"No columns found for table {tableName} in schema {schema}")
    def zip_rows(self, tableName, rows, schema='public'):
        column_names = self.get_column_names(tableName, schema)
        if rows:
            return [dict(zip(columnNames,make_list(row))) for row in rows]
def get_column_names(tableName,schema='public'):
    return columnNamesManager().get_column_names(tableName,schema)
def getZipRows(tableName, rows, schema='public'):
    columnNames = get_column_names(tableName,schema)
    if columnNames:
        return [dict(zip(columnNames,row)) for row in make_list(rows) if row]
def get_db_from(tableName=None,columnNames=None,searchColumn=None,searchValue=None,count=False,zipit=True):
    columnNames=columnNames or '*'
    if isinstance(columnNames,list):
        columnNames = ','.join(columnNames)
    response = fetch_any_combo(tableName=tableName,columnNames=columnNames,searchColumn=searchColumn,searchValue=searchValue,zipit=zipit,count=count)
    return response
def get_all_table_info(schema='public'):
    all_table_infos = {each:get_column_names(each) for each in get_all_table_names()}
    return all_table_infos

