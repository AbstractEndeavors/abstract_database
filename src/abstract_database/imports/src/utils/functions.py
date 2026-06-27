from .imports import *
def manage_db():
    manageDb(dbUrl=get_db_url())
def get_from_db(freshCall,tableName,searchValue,fetch_from_db):
    if not freshCall:
        insertValue  = fetch_from_db(tableName=tableName,searchValue=searchValue)
        if insertValue:
            return insertValue

def find_latest_index():
    df_mgr = dfManager()
    last_row = get_last_row("realestatedata")
    if last_row:
        search_address = last_row[1]
        for index, row in df_mgr.df.iterrows():
            if search_address == df_mgr.get_address_from_row(row):
                return index
    return 0
def query_table(dbName,*args,**kwargs) -> None:
    with get_engine(dbName).connect() as conn:
        try:
            conn.execute(*args,**kwargs)
            conn.commit()
        except SQLAlchemyError as e:
            print(f"Failed to insert data: {e}")
            return e
def get_browser_mgr():
    data_brswr = DatabaseBrowser(dbUrl=get_db_url())
    return data_brswr
def ensure_table_exists(dbName,tableName):
    table = get_table(tableName)
    query_table(dbName,get_browser_mgr(), table.get('table'))
def delete_table(tableName):
    get_browser_mgr().delete_table(tableName.replace('_','').lower())
def view_table(tableName):
    brows_mgr = get_browser_mgr()
    table_row_count = brows_mgr.session.execute(text(f"SELECT COUNT(*) FROM {tableName}")).scalar()
    if table_row_count:
        brows_mgr.view_table(tableName, table_row_count-1, table_row_count)
def insertintodefaultvalues(dbName,insertTable,key=None, value=None,tableName=None):
    #ensure_table_exists(tableName)
    key_key = insertTable.get('columnSearch')
    insertName=insertTable.get('insertName')
    tableName = insertTable.get('tableName')
    # Adjusted insert query using consistent parameter style
    insert_query = text(f"""
    INSERT INTO {tableName} ({key_key}, {insertName}, last_updated)
    VALUES (:{key_key}, :{insertName}, NOW())
    ON CONFLICT ({key_key}) DO UPDATE
    SET {insertName} = EXCLUDED.{insertName}, last_updated = NOW()
    WHERE {tableName}.{insertName} != EXCLUDED.{insertName};
    """)
    # Convert value toinput JSON string if it's not a JSON-compatible type
    json_value = Json(value) if isany_instance(value) else Json(f'{value}')
    key_value = str(key) if isany_instance(key) else str(f'{key}')
    # Connect to the database using SQLAlchemy
    e = query_table(dbName,insert_query, {key_key: key_value, insertName: json_value})
    if e is None:
        print(f"Inserted ({key}, value) as json_value successfully.")
def resolve_as_dict(**kwargs):
    for key in ['as_dict', 'zipRows', 'zipit']:
        value = kwargs.get(key)
        if isinstance(value,bool):
            return value
