from .imports import *
from .pairs import get_any_pair
def get_metadata_from(columnNames=None,searchColumn=None,searchValue=None,count=False,zipit=True):
    columnNames = columnNames or '*'
    return get_db_from(tableName='metadata',
                       columnNames=columnNames,
                       searchColumn=searchColumn,
                       searchValue=searchValue,
                       count=count,
                       zipit=zipit)
def get_meta_data_from_mint(mint,columnNames=None,zipit=True):
    return get_metadata_from(searchColumn='mint', searchValue=mint,columnNames=columnNames,zipit=zipit)
def get_meta_data_from_meta_id(meta_id,columnNames=None,zipit=True):
    return get_metadata_from(searchColumn='id', searchValue=meta_id,columnNames=columnNames,zipit=zipit)
def get_meta_data_from_pair(pair_data,columnNames=None,zipit=True):
    pair = get_any_pair(pair_data,zipit=zipit)
    meta_id = pair.get('meta_id')
    if not meta_id:
        return []
    return get_meta_data_from_meta_id(meta_id,columnNames=columnNames,zipit=zipit)
#####################################
# Fix #4: get_meta_data uses correct references
#####################################
def get_meta_data(pair_id=None, meta_id=None, mint=None,zipit=True):
    if mint:
        return get_meta_data_from_mint(mint,zipit=zipit)
    if pair_id:
        return get_meta_data_from_pair(pair_id,zipit=zipit)
    if meta_id:
        return get_meta_data_from_meta_id(meta_id,zipit=zipit)
    return []
