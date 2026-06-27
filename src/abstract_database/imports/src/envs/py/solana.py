# src/env/solana.py
from .imports import *

_SOLANA_DISPLAYED = False





def require_int(
    key: str,
    env_path=None,
    fallback: str | None = None,
) -> int:
    return int(require_env(key=key, env_path=env_path, fallback=fallback))


def load_solana_env(env_path=None) -> dict:
    global _SOLANA_DISPLAYED

    out = {
        "pumpFunProgramId": require_env(
            key="SOLCATCHER_SOLANA_PUMP_FUN_PROGRAM_ID",
            fallback="6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
            env_path=env_path,
        ),

        "dbMaxClients": require_int(
            key="SOLCATCHER_SOLANA_DB_MAX_CLIENTS",
            fallback="5",
            env_path=env_path,
        ),
        "idleTimeoutMs": require_int(
            key="SOLCATCHER_SOLANA_IDLE_TIMEOUT_MS",
            fallback="30000",
            env_path=env_path,
        ),
        "connectionTimeoutMs": require_int(
            key="SOLCATCHER_SOLANA_CONNECTION_TIMEOUT_MS",
            fallback="2000",
            env_path=env_path,
        ),
        "batchSize": require_int(
            key="SOLCATCHER_SOLANA_BATCH_SIZE",
            fallback="10",
            env_path=env_path,
        ),
        "pauseDurationMs": require_int(
            key="SOLCATCHER_SOLANA_PAUSE_DURATION_MS",
            fallback="20000",
            env_path=env_path,
        ),

        "metaplexToken": require_env(
            key="SOLCATCHER_SOLANA_METAPLEX_TOKEN",
            fallback="METAewgxyPbgwsseH8T16a39CQ5VyVxZi9zXiDPY18m",
            env_path=env_path,
        ),
        "computeBudget": require_env(
            key="SOLCATCHER_SOLANA_COMPUTE_BUDGET",
            fallback="ComputeBudget111111111111111111111111111111",
            env_path=env_path,
        ),
        "jupiterAggregator": require_env(
            key="SOLCATCHER_SOLANA_JUPITER_AGGREGATOR",
            fallback="JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
            env_path=env_path,
        ),
        "usdcMint": require_env(
            key="SOLCATCHER_SOLANA_USDC_MINT",
            fallback="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            env_path=env_path,
        ),
        "pumpFunAccount": require_env(
            key="SOLCATCHER_SOLANA_PUMP_FUN_ACCOUNT",
            fallback="Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1",
            env_path=env_path,
        ),
        "tokenProgram": require_env(
            key="SOLCATCHER_SOLANA_TOKEN_PROGRAM",
            fallback="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
            env_path=env_path,
        ),
        "raydiumPoolV4ProgramId": require_env(
            key="SOLCATCHER_SOLANA_RAYDIUM_POOL_V4_PROGRAM_ID",
            fallback="675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
            env_path=env_path,
        ),
        "solanaMint": require_env(
            key="SOLCATCHER_SOLANA_MINT",
            fallback="So11111111111111111111111111111111111111112",
            env_path=env_path,
        ),

        "solDecimals": require_int(
            key="SOLCATCHER_SOLANA_SOL_DECIMALS",
            fallback="9",
            env_path=env_path,
        ),
        "solLamports": require_int(
            key="SOLCATCHER_SOLANA_SOL_LAMPORTS",
            fallback="1000000000",
            env_path=env_path,
        ),

        "rpcUrl": require_env(
            key="SOLCATCHER_SOLANA_RPC_URL",
            fallback="https://api.mainnet-beta.solana.com",
            env_path=env_path,
        ),
        "fallbackRpcUrl": require_env(
            key="SOLCATCHER_SOLANA_FALLBACK_RPC_URL",
            fallback="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",
            env_path=env_path,
        ),
        "wsUrl": require_env(
            key="SOLCATCHER_SOLANA_WS_ENDPOINT",
            fallback="wss://api.mainnet-beta.solana.com",
            env_path=env_path,
        ),
        "fallbackWsUrl": require_env(
            key="SOLCATCHER_SOLANA_FALLBACK_WS_ENDPOINT",
            fallback="wss://rpc.ankr.com/solana/ws/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",
            env_path=env_path,
        ),
        "mainnetRpcUrl": require_env(
            key="SOLCATCHER_SOLANA_MAINNET_RPC_URL",
            fallback="https://api.mainnet-beta.solana.com",
            env_path=env_path,
        ),
        "broadcastPort": require_int(
            key="SOLCATCHER_WS_BROADCAST_PORT",
            fallback="6047",
            env_path=env_path,
        ),
    }

    if not _SOLANA_DISPLAYED:
        print(out)
        _SOLANA_DISPLAYED = True

    return out
