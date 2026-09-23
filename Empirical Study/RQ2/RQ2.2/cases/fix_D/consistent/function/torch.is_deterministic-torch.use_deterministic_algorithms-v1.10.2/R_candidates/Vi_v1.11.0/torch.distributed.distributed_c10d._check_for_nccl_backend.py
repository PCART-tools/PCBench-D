def _check_for_nccl_backend(group):
    pg = group or _get_default_group()
    # It is not expected for PG to be wrapped many times, but support it just
    # in case
    while isinstance(pg, _ProcessGroupWrapper):
        pg = pg.wrapped_pg

    return (
        is_nccl_available() and
        isinstance(pg, ProcessGroupNCCL)
    )
