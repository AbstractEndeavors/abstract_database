from .imports import *
def fetchmeta(mint):
    meta_data = asyncio.run(async_call_solcatcher_ts('get-metadata-foundation',mint=mint,url=ankr_url,get_id=False))
    
    return get_meta_data_from_meta_id(meta_data)
def get_or_fetch_meta(mint):
    meta_data = asyncio.run(async_call_solcatcher_ts('get-or-fetch-metadata',mint=mint))
    return meta_data
