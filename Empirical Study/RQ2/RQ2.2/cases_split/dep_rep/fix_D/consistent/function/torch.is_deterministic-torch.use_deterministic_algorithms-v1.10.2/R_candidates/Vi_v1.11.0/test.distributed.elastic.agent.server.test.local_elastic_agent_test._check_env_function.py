def _check_env_function():
    # just check these env vars exist, os.environ[...] will naturally throw
    # if the variable does not exist
    env_vars = [
        "RANK",
        "LOCAL_RANK",
        "ROLE_RANK",
        "ROLE_NAME",
        "GROUP_RANK",
        "LOCAL_WORLD_SIZE",
        "ROLE_WORLD_SIZE",
        "WORLD_SIZE",
        "GROUP_WORLD_SIZE",
        "MASTER_ADDR",
        "MASTER_PORT",
        "TORCHELASTIC_RESTART_COUNT",
        "TORCHELASTIC_MAX_RESTARTS",
        "TORCHELASTIC_RUN_ID",
        "TORCHELASTIC_USE_AGENT_STORE",
    ]
    for var in env_vars:
        _ = os.environ[var]
