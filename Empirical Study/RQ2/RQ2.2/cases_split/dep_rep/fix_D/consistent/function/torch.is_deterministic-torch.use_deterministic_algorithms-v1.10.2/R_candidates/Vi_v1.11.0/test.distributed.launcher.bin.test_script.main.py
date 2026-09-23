def main():
    args = parse_args()
    env_vars = [
        "LOCAL_RANK",
        "RANK",
        "GROUP_RANK",
        "ROLE_RANK",
        "ROLE_NAME",
        "LOCAL_WORLD_SIZE",
        "WORLD_SIZE",
        "ROLE_WORLD_SIZE",
        "MASTER_ADDR",
        "MASTER_PORT",
        "TORCHELASTIC_RESTART_COUNT",
        "TORCHELASTIC_MAX_RESTARTS",
        "TORCHELASTIC_RUN_ID",
        "OMP_NUM_THREADS",
        "TEST_SENTINEL_PARENT",
        "TORCHELASTIC_ERROR_FILE",
    ]

    print("Distributed env vars set by agent:")
    for env_var in env_vars:
        value = os.environ[env_var]
        print(f"{env_var} = {value}")

    if args.fail:
        raise RuntimeError("raising exception since --fail flag was set")
    else:
        file = os.path.join(args.touch_file_dir, os.environ["RANK"])
        Path(file).touch()
        print(f"Success, created {file}")
