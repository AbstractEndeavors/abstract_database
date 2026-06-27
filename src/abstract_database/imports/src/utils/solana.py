from .imports import *
def get_if_list(obj):
    if obj and isinstance(obj,list):
        return obj[0]
def get_mint_length():
    mint_length = len('E3HurESTBHNed6HnARSMBg45i9va2d9BYeZMcnsQpump')
    return mint_length
def get_signature_length():
    signature = len('34WyijxfHuoabvHpmHFNxrBvGwRXy12vdtbDvt4bQThdALEWyRYqN39VMyncXC3FoYK8BVBP39ahws7z615jZ45T')
    return signature
def is_mint(obj):
    if isinstance(obj,str):
        return len(obj) == get_mint_length()
    return False
def is_signature(obj):
    if isinstance(obj,str):
        return len(obj) == get_signature_length()
    return False
def if_list_get_single(obj):
    while True:
        if obj != None and isinstance(obj,list) and len(obj) == 1:
            obj = obj[0]
        else:
            break
    
    return obj
def get_zero_or_real(obj):
    while True:
        if isinstance(obj,list) and len(obj) == 1:
            obj = if_list_get_single(obj)
        else:
            break
    if isinstance(obj,list) and len(obj) > 1:
        obj = obj[0]
    return obj or 0
def get_key_value(txn,key):
    if isinstance(txn, list):
        if txn and 'tcns' in txn[0]:
            return get_any_value(txn[0]['tcns'], key)
        else:
            txn = if_list_get_single(txn)
    return get_any_value(txn, key)
def flatten_txn(txn):
    txns = []
    for tcn in get_any_value(txn,'tcns') or []:
        new_txn = {**txn, **tcn}
        if 'tcns' in new_txn:
            del new_txn['tcns']
        txns.append(new_txn)
    return if_list_get_single(txns or txn)
def flatten_txn_history(txns):
    return [flatten_txn(txn) for txn in txns or [] if txn]
def sort_txn_history(txns):
    sorted_txns = sorted(txns, key=lambda txn: get_timestamps(txn))
    return sorted_txns
def get_sorted_txn_history(txns):
    txns = flatten_txn_history(txns)
    sorted_txns = sort_txn_history(txns)
    return sorted_txns
def get_string_value(txn,key):
    value = get_key_value(txn,key)
    if isinstance(value,list):
        value = list(set(value))
    return if_list_get_single(value)
def get_integer_value(txn,key):
    value = get_key_value(txn,key)
    return get_zero_or_real(value)
def get_bool_value(txn,key):
    value = get_key_value(txn,key)
    return if_list_get_single(value)
def get_txn_price(txn):
    return get_integer_value(txn,'price')
def get_virtual_sol_reserves(txn):
    return get_key_value(txn,'virtual_sol_reserves')
def get_virtual_token_reserves(txn):
    return get_key_value(txn,'virtual_token_reserves')
def get_user_address(txn):
    return get_string_value(txn,'user_address')
def get_mint(txn):
    return get_string_value(txn,'mint')
def get_bonding_curve(txn):
    return get_string_value(txn,'bonding_curve')
def get_timestamps(txn):
    return get_integer_value(txn,'timestamp')
def get_sol_amount(txn):
    return get_integer_value(txn,'sol_amount')
def get_supply(txn):
    value = get_integer_value(txn,'supply')
    if not value:
        value = get_key_value(txn,'supply')
    return value
def get_token_amount(txn):
    return get_integer_value(txn,'token_amount')
def get_is_buy(txn):
    return get_bool_value(txn,'is_buy')
def get_signature(txn):
    return get_string_value(txn,'signature')
def get_all_timestamps(txns):
    timestamps = [get_timestamps(txn) for txn in txns]
    timestamps.sort()
    return timestamps
def get_price(virtualSolReserves, virtualTokenReserves):
    return divide_it(virtualSolReserves,virtualTokenReserves)
def get_any_function(txn,key):
    result=None
    key_lower = key.lower().replace(' ','_')
    funcs_js = {'price': get_txn_price,
     'virtual_sol_reserves': get_virtual_sol_reserves,
     'virtual_token_reserves': get_virtual_token_reserves,
     'user_address': get_user_address,
     'mint': get_mint,
     'bonding_curve': get_bonding_curve,
     'timestamp': get_timestamps,
     'sol_amount': get_sol_amount,
     'supply': get_supply,
     'token_amount': get_token_amount,
     'is_buy': get_is_buy,
     'signature':get_signature}
    func = funcs_js.get(key_lower)
    if func:
        result = func(txn)
    
    else:
        flattened_txn= flatten_txn(txn)
        flattened_txn = get_if_list(flattened_txn)
        if flattened_txn:
            result = get_key_value(flattened_txn,key)
            if result in [None,[]]:
                result = flattened_txn.get(key)
    return result

    
