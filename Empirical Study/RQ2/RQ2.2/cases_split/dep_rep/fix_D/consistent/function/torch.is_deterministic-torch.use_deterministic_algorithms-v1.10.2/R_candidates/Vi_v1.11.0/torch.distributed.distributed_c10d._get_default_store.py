def _get_default_store():
    """
    Getting the default store created by init_process_group
    """
    if not is_initialized():
        raise RuntimeError(
            "Default process group has not been initialized, "
            "please make sure to call init_process_group."
        )
    default_pg = _get_default_group()
    _, default_store = _pg_map[default_pg]
    return default_store
