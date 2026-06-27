from .imports import *
from .logdata import get_logdata_from_signature
from .transactions import get_transactions
def get_creation_txn(txn_id=None,log_id=None,signature=None,pair_id=None):
    txns = get_transactions(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    txns = get_sorted_txn_history(txns)
    txns = if_list_get_single(txns)
    return txns
def get_creation_signature(txn_id=None,log_id=None,signature=None,pair_id=None):
    creation_txns = get_creation_txn(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    creation_txn = make_list(creation_txns)
    if creation_txn and len(creation_txn)>0:
        creation_txn = creation_txn[0]
        creation_signature = get_signature(creation_txn)
        return creation_signature
def get_creation_logdata(txn_id=None,log_id=None,signature=None,pair_id=None):
    creation_signature = get_creation_signature(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    log_data  =get_logdata_from_signature(creation_signature)
    return log_data
def get_creation_logs(txn_id=None,log_id=None,signature=None,pair_id=None):
    log_data = get_creation_logdata(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    log_data = if_list_get_single(log_data)
    logs = get_any_value(log_data,'logs')
    logs = logs[0]
    return logs
def get_creation_log_data(txn_id=None,log_id=None,signature=None,pair_id=None):
    logs = get_creation_logs(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    creation_logs = [log for log in logs if log and log.get('data') and log.get('logs') and "Instruction: Create" in log.get('logs')]
    return creation_logs
def get_creation_data(txn_id=None,log_id=None,signature=None,pair_id=None):
    creation_logs = get_creation_log_data(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    for log in creation_logs:
        data = log.get('data')
        if data:
            return data[0]
def get_creation_decoded_data(txn_id=None,log_id=None,signature=None,pair_id=None):
    print(f"creation data: txn_id={txn_id},log_id={log_id},signature={signature},pair_id={pair_id}")
    creation_data = get_creation_data(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    if creation_data:
        decoded_data = call_solcatcher_ts('decode-instruction-data',data=creation_data)
        if decoded_data:
            return decoded_data
def get_creation_program_id(txn_id=None,log_id=None,signature=None,pair_id=None):
    log_data = get_creation_logdata(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    log_data = if_list_get_single(log_data)
    program_id = log_data.get('program_id')
    if not program_id:
        logs = log_data.get('logs')
        for log in logs:
            data = log.get('data')
            if data:
                program_id = log.get('program_id')
            if program_id:
                return program_id
    return program_id
def get_creation_bonding_curve(txn_id=None,log_id=None,signature=None,pair_id=None):
    decoded_data = get_creation_decoded_data(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    if decoded_data:
        return decoded_data.get('bonding_curve')
def get_creation_user_address(txn_id=None,log_id=None,signature=None,pair_id=None):
    decoded_data = get_creation_decoded_data(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    if decoded_data:
        return decoded_data.get('user_address')
def get_creation_mint(txn_id=None,log_id=None,signature=None,pair_id=None):
    decoded_data = get_creation_decoded_data(txn_id=txn_id,log_id=log_id,signature=signature,pair_id=pair_id)
    if decoded_data:
        return decoded_data.get('mint')
def get_txn_history_from_selected_row(selected_row: Dict[str, Any]) -> Tuple[Any, Any]:
    """
    Returns the pair_id and transaction history based on the selected row.
    """
    pair_id = get_any_value(selected_row, 'pair_id')
    txn_history = fetch_any_combo(tableName='transactions',searchColumn='pair_id',searchValue=pair_id)
    return pair_id, txn_history

def get_signature_transaction(signature: str) -> Any:
    """
    Returns the transaction (as a list if needed) corresponding to a signature.
    """
    txn = get_transactions(signature=signature)
    return get_if_list(txn)
