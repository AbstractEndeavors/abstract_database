from ..src import *
values = get_db_env_value(dbName='abstract_base',env_path=os.path.join(get_caller_dir(),'.env'))
input(values)
