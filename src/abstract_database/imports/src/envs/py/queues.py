# src/env/queues.py
from .imports import *

_QUEUE_DISPLAYED = False


def load_queue_env(env_path=None) -> dict:
    global _QUEUE_DISPLAYED

    out = {
        "workerName": require_env(key="SOLCATCHER_QUEUE_NAME",fallback="solcatcher",env_path=env_path),

        "vhost": require_env(key="SOLCATCHER_QUEUE_VHOST",fallback="solcatcher",env_path=env_path),
        "logIntake": require_env(key="SOLCATCHER_QUEUE_LOG_INTAKE",fallback="logIntakeQueue",env_path=env_path),
        "logEntry": require_env(key="SOLCATCHER_QUEUE_LOG_ENTRY",fallback="logEntryQueue",env_path=env_path),
        "txnEntry": require_env(key="SOLCATCHER_QUEUE_TXN_ENTRY",fallback="txnEntryQueue",env_path=env_path),

        "metadataGenesisEnrich": require_env(key=
            "SOLCATCHER_QUEUE_METADATA_GENESIS_ENRICH_QUEUE",fallback="metadataGenesisEnrichQueue"
        ,env_path=env_path),
        "metadataUriEnrich": require_env(key=
            "SOLCATCHER_QUEUE_METADATA_URI_ENRICH_QUEUE",fallback="metadataUriEnrichQueue"
        ,env_path=env_path),

        "signatureCall": require_env(key="SOLCATCHER_QUEUE_SIGNATURE_CALL",fallback="signatureCallQueue",env_path=env_path),
        "metaDataCall": require_env(key="SOLCATCHER_QUEUE_META_DATA_CALL",fallback="metaDataCallQueue",env_path=env_path),
        "pairCall": require_env(key="SOLCATCHER_QUEUE_PAIR_ENTRY",fallback="pairCallQueue",env_path=env_path),
        "signatureGenesisCall": require_env(key=
            "SOLCATCHER_QUEUE_SIGNATURE_GENESIS_CALL",fallback="signatureGenesisCallQueue"
        ,env_path=env_path),
        "rpcCall": require_env(key="SOLCATCHER_QUEUE_RPC_CALL",fallback="rpcCallQueue",env_path=env_path),
        "transactionCall": require_env(key="SOLCATCHER_QUEUE_TRANSACTION_CALL",fallback="transactionCallQueue",env_path=env_path),
        "getSignaturesCall": require_env(key=
            "SOLCATCHER_QUEUE_GET_SIGNATURES_CALL",fallback="getSignaturesCallQueue"
        ,env_path=env_path),
    }

    if not _QUEUE_DISPLAYED:
        print("📦 Queue config:", out)
        _QUEUE_DISPLAYED = True

    return out
