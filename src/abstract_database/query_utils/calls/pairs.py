from .imports import *
def get_pair_from(searchColumn,searchValue,zipit=True):
    response = fetch_any_combo(tableName='pairs',searchColumn=searchColumn,searchValue=searchValue,zipit=zipit)
    return response
def get_pair_from_mint(mint,zipit=True):
    return get_pair_from(searchColumn="mint",searchValue=mint,zipit=zipit)
def get_pair_from_signature(signature,zipit=True):
    return get_pair_from(searchColumn="signature",searchValue=signature,zipit=zipit)
def get_pair_from_pair_id(pair_id,zipit=True):
    return get_pair_from(searchColumn="id",searchValue=pair_id,zipit=zipit)
def get_pair(mint=None,signature=None,pair_id=None,zipit=True):
    if mint:
        return get_pair_from_mint(mint,zipit=zipit)
    if signature:
        return get_pair_from_signature(signature,zipit=zipit)
    if pair_id:
        return get_pair_from_pair_id(pair_id,zipit=zipit)
def get_any_pair(obj,zipit=True):
    pair_id=None
    signature=None
    mint=None
    pair = []
    if isinstance(obj,int):
        pair_id = obj
    elif is_signature(obj):
        signature = obj
    elif is_mint(obj):
        mint = obj
    elif isinstance(obj,dict or list):
        pair = obj
    if pair == []:
        pair = get_pair(mint=mint,signature=signature,pair_id=pair_id,zipit=zipit)
    if pair:
        pair = if_list_get_single(pair)
    return pair
def get_all_pair_data(mint=None,signature=None,pair_id=None):
    pair_data = {}
    pair = get_pair(mint=mint,signature=signature,pair_id=pair_id,zipit=True)
    pair_id = pair.get('id')
    mint = pair.get('mint')
    pair_data["pair"] = pair
    pair_data["txns"] = get_transactions(pair_id=pair_id)
    pair_data["metadata"] = get_meta_data(mint=mint)
    return pair_data
def get_all_txns_for_pair_id(pair_id): 
    response = fetch_any_combo(tableName='transactions',searchColumn='pair_id',searchValue=pair_id,zipit=True)
    return response
