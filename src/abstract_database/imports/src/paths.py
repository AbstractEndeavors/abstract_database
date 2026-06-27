from .init_imports import os,yaml,safe_load_from_json,get_caller_dir
def get_imports_dir():
    return get_caller_dir()
def get_abstract_database_dir():
    imports_dir = get_imports_dir()
    return os.path.dirname(imports_dir)
def get_query_utils_dir():
    abstract_database_dir = get_abstract_database_dir()
    return os.path.join(query_utils_dir,'query_utils')
def get_queries_dir():
    query_utils_dir = get_query_utils_dir()
    queries_dir = os.path.join(query_utils_dir,'queries')
    return queries_dir
def get_yaml_queries_path():
    queries_dir = get_queries_dir()
    yaml_queries_path = os.path.join(queries_dir,'queries.yaml')
    return yaml_queries_path
def get_queries_json_dir():
    queries_dir = get_queries_dir()
    json_queries_dir = os.path.join(queries_dir,'json_queries')
    return json_queries_dir
def get_json_queries_path(basename):
    queries_json_dir = get_queries_json_dir()
    json_queries_path = os.path.join(queries_json_dir,basename)
    return json_queries_path
def get_json_queries_data(basename):
    json_queries_path = get_json_queries_path(basename)
    if json_queries_path and os.path.isfile(json_queries_path):
        data = safe_load_from_json(user_queries_path)
        return data
def get_yaml_queries_data(data_type):
    """Load blacklist queries from the YAML file."""
    yaml_path =get_yaml_queries_path()
    try:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file) or {}
            return data.get(data_type, data)
    except Exception as e:
        print(f"Error loading YAML file {yaml_path}: {e}")
        return {}
