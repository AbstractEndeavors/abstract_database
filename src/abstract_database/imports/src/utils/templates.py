from .imports import *
def get_value_type(value):
    if is_number(value):
        if '.' in str(value):
            value = float(value)
        else:
            value = int(value)
        if isinstance(value, int):
            return "INTEGER"
        if isinstance(value, float):
            return "REAL"
    if isinstance(value, list):
        return "ARRAY"
    if isinstance(value, dict):
        return "JSON"
    if isinstance(value, bool):
        return "BOOL"
    return "TEXT"
def is_timestamp_key(key):
    return False
    try:
        float(key)
        return True
    except ValueError:
        return False
def get_value_keys(data):
    value_keys = {}
    if isinstance(data,dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # Special case for dictionaries with timestamp keys
                value_keys[key] = get_value_keys(value)
            else:
                value_keys[key] = get_value_type(value)
    else:
        value_keys['signnature']=get_value_type(data)
    return value_keys
def get_unique(data):
    keys = ["signature","address","blockTime"]
    if isinstance(data,dict):
        for key,value in data.items():
            for unique_key in keys:
                if unique_key in str(key).lower():
                    return [key]
    return []
def create_templates(dbName,templates_dir=None,dbDir=None,varDir=None):
    all_table_dicts = {dbName:{}}
    dirName = templates_dir or os.path.join(os.getcwd(),"templates")
    dbDir = dbDir or os.path.join(os.getcwd(),"database")
    os.makedirs(dbDir,exist_ok=True)
    dbVarsDir = varDir or os.path.join(dbDir,"variabels")
    os.makedirs(dbVarsDir,exist_ok=True)
    for baseName in os.listdir(dirName):
         filePath = os.path.join(dirName,baseName)
         if os.path.isfile(filePath):
             fileName,ext = os.path.splitext(baseName)
             if ext == '.json' and filePath and os.path.isfile(filePath):
                 data = safe_json_loads(safe_load_from_json(file_path=filePath))
                 all_table_dicts[dbName][fileName]={"valueKeys":get_value_keys(data),"unique_keys" : get_unique(data)}            
    dbFilePath = os.path.join(dbVarsDir,'dbVars.json')
    safe_dump_to_file(data=all_table_dicts,file_path=dbFilePath)
    return dbFilePath
def dump_if_json(obj):
    return json.dumps(obj) if isinstance(obj, dict) else obj
