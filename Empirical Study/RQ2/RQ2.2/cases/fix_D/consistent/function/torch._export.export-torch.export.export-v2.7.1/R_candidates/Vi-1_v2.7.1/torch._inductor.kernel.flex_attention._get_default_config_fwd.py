def _get_default_config_fwd(query) -> tuple[int, int, int, int]:
    if torch.version.hip is None:
        return _get_nv_config(query, mode=Mode.fwd)
    else:
        return _get_rocm_config(query, mode=Mode.fwd)
