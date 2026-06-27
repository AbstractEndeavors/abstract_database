from .imports import SingletonMeta
class sessionManager(metaclass=SingletonMeta):
    def __init__(self, Base=None,db_vars=None,dbDir=None):
        self.dbTracker = {}
        self.Base = Base or declarative_base()
        self.db_vars=db_vars or {}
        self.dbDir=dbDir or os.path.join(os.getcwd(),"databases")
        self.initialize_all_dbs()
    def initialize_all_dbs(self):
        for dbName, db_info in self.db_vars.items():
            dbPath = os.path.join(self.dbDir,f"{dbName}.db")
            dbName = get_db_name(dbPath=dbPath, dbUrl=get_db_url(dbPath))
            self.initialize_db(dbName=dbName,dbPath=dbPath, db_tables=db_info)
    def initialize_db(self,dbName=None, dbPath=None, dbUrl=None, db_tables=None):
        dbUrl = dbUrl or get_db_url(dbPath)
        
        self.checkDatabaseName(dbName=dbName, dbPath=dbPath, dbUrl=dbUrl, db_tables=self.db_vars[dbName])
        self.create_session(dbPath=dbPath, dbUrl=dbUrl)
        self.create_tables(dbName)
        return dbName

    def get_dbName(self, dbName=None, dbPath=None, dbUrl=None):
        if dbName is None and dbUrl is None and dbPath is None:
            return dbName
        elif dbName is None and (dbUrl is not None or dbPath is not None):
            dbName = get_db_name(dbPath=dbPath, dbUrl=dbUrl)
        return dbName

    def create_session(self, dbPath=None, dbUrl=None):
        dbName = get_db_name(dbPath=dbPath, dbUrl=dbUrl)
        self.dbTracker[dbName]["engine"] = get_db_engine(dbUrl=dbUrl, dbPath=dbPath)
        self.Base.metadata.bind = self.dbTracker[dbName]["engine"]
        self.solcatcherDBSession = sessionmaker(bind=self.dbTracker[dbName]["engine"])
        self.dbTracker[dbName]["session"] = self.solcatcherDBSession()

    def create_tables(self, dbName=None, dbPath=None, dbUrl=None):
        self.Base.metadata.create_all(self.dbTracker[dbName]["engine"])
        dbName = get_db_name(dbName=dbName, dbPath=dbPath, dbUrl=dbUrl)
        for table, columns_info in self.dbTracker[dbName]["db_tables"].items():
            columns = list(columns_info["valueKeys"].keys())
            columns_defs = self.flatten_columns_defs(columns_info["valueKeys"])
            create_table_sql = text(f'CREATE TABLE IF NOT EXISTS "{table}" ({columns_defs});')
            self.dbTracker[dbName]["session"].execute(create_table_sql)
        self.dbTracker[dbName]["session"].commit()


    def flatten_columns_defs(self, valueKeys):
        column_defs = []
        for col, dtype in valueKeys.items():
            col_name = f'"{col}"'
            if isinstance(dtype, dict):
                column_defs.append(f"{col_name} JSON")
            elif isinstance(dtype, list):
                column_defs.append(f"{col_name} JSON")
            else:
                column_defs.append(f"{col_name} {dtype}")
        return ", ".join(column_defs)

    def checkDatabaseName(self, dbName=None, dbPath=None, dbUrl=None, dbBrowser=None, db_tables=None, primary_types=None):
        dbName = self.get_dbName(dbName=dbName, dbPath=dbPath, dbUrl=dbUrl)
        if dbName not in self.dbTracker:
            self.dbTracker[dbName] = {"dbUrl": dbUrl, "dbPath": dbPath, "db_tables": db_tables, "columns_info": self.db_vars.get(dbName),"classes":{}}
            for key,value in self.db_vars.get(dbName).items():
                self.dbTracker[dbName]["classes"][key] = create_class_from_dict(capitalize(key), value,self.Base)
                
    def close_session(self, dbName=None, dbPath=None, dbUrl=None):
        dbName = self.get_dbName(dbName=dbName, dbPath=dbPath, dbUrl=dbUrl)
        self.dbTracker[dbName]["session"].close()

    # Function to insert a record
    def insert_record(self, dbName, class_name, record, unique_keys=None):
        model = self.dbTracker[dbName]["classes"][class_name]
        session = self.dbTracker[dbName]["session"]
        unique_keys=make_list(unique_keys or self.dbTracker[dbName]["columns_info"][class_name]['unique_keys'])
        if record_exists(session, model, **{key: record[key] for key in unique_keys}):
            #print(f"Duplicate entry found with keys: {unique_keys}. Skipping...")
            return
        new_record = model(**record)
        try:
            session.add(new_record)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Integrity error for record: {record}. Rolling back transaction.")


    # Function to update a record
    def update_record(self, dbName, table_name, record, conditions):
        session = self.dbTracker[dbName]["session"]
        set_clause = ", ".join([f'"{key}" = :{key}' for key in record.keys()])
        condition_clause = " AND ".join([f'"{key}" = :{key}' for key in conditions.keys()])
        update_sql = text(f'UPDATE "{table_name}" SET {set_clause} WHERE {condition_clause}')
        session.execute(update_sql, {**record, **conditions})
        session.commit()

    # Function to delete a record
    def delete_record(self, dbName, table_name, conditions):
        session = self.dbTracker[dbName]["session"]
        condition_clause = " AND ".join([f'"{key}" = :{key}' for key in conditions.keys()])
        delete_sql = text(f'DELETE FROM "{table_name}" WHERE {condition_clause}')
        session.execute(delete_sql, conditions)
        session.commit()
