from .imports import *
def get_logdata_from(columnNames=None,searchColumn=None,searchValue=None,count=False,zipit=True):
    columnNames = columnNames or '*'
    return get_db_from(tableName='logdata',
                       columnNames=columnNames,
                       searchColumn=searchColumn,
                       searchValue=searchValue,
                       count=count,
                       zipit=zipit)
def get_logdata_from_log_id(log_id,zipit=True):
    return get_logdata_from(searchColumn='id',searchValue=log_id,zipit=zipit)
def get_signature_from_log_id(log_id,zipit=True):
    return get_logdata_from(columnNames='signature',searchColumn='id',searchValue=log_id,zipit=zipit)
def get_logdata_from_signature(signature,zipit=True):
    return get_logdata_from(columnNames='*',searchColumn='signature',searchValue=signature,zipit=zipit)

                    
