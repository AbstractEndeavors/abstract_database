from .imports import get_db_from,fetch_any_combo
from .logdata import get_signature_from_log_id
def get_transaction_from(columnNames=None,searchColumn=None,searchValue=None,count=False,zipit=True):
    columnNames = columnNames or '*'
    return get_db_from(tableName='transactions',
                       columnNames=columnNames,
                       searchColumn=searchColumn,
                       searchValue=searchValue,
                       count=count,
                       zipit=zipit)
def count_transactions_for_pair(pair_id,zipit=True):
    return get_transaction_from(searchColumn="pair_id",searchValue=pair_id,count=True,zipit=zipit)
def get_transaction_from_signature(signature,zipit=True):
    return get_transaction_from(searchColumn="signature",searchValue=signature,zipit=zipit)
def get_transaction_from_txn_id(txn_id,zipit=True):
    return get_transaction_from(searchColumn="id",searchValue=txn_id,zipit=zipit)
def get_transaction_from_log_id(log_id,zipit=True):
    signature = get_signature_from_log_id(log_id,zipit=zipit)
    return get_transaction_from_signature(signature,zipit=zipit)
def get_all_txns_from_pair_id(pair_id,zipit=True):
    return get_transaction_from(searchColumn="pair_id",searchValue=pair_id,zipit=zipit)
def get_transactions(txn_id=None,log_id=None,signature=None,pair_id=None,zipit=True):
    if pair_id:
        return get_all_txns_from_pair_id(pair_id,zipit=zipit)
    if txn_id:
        return get_transaction_from_txn_id(txn_id,zipit=zipit)
    if log_id:
        return get_transaction_from_log_id(log_id,zipit=zipit)
    if signature:
        return get_transaction_from_signature(signature,zipit=zipit)

