def check_free_memory(free_bytes):
    """
    Check whether `free_bytes` amount of memory is currently free.
    Returns: None if enough memory available, otherwise error message
    """
    env_var = "NPY_AVAILABLE_MEM"
    env_value = os.environ.get(env_var)
    if env_value is not None:
        try:
            mem_free = _parse_size(env_value)
        except ValueError as exc:
            raise ValueError(  # noqa: B904
                f"Invalid environment variable {env_var}: {exc}"
            )

        msg = (
            f"{free_bytes / 1e9} GB memory required, but environment variable "
            f"NPY_AVAILABLE_MEM={env_value} set"
        )
    else:
        mem_free = _get_mem_available()

        if mem_free is None:
            msg = (
                "Could not determine available memory; set NPY_AVAILABLE_MEM "
                "environment variable (e.g. NPY_AVAILABLE_MEM=16GB) to run "
                "the test."
            )
            mem_free = -1
        else:
            msg = f"{free_bytes / 1e9} GB memory required, but {mem_free / 1e9} GB available"

    return msg if mem_free < free_bytes else None
