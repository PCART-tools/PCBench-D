def fx_graph_remote_cache_default() -> Optional[bool]:
    return get_tristate_env("TORCHINDUCTOR_FX_GRAPH_REMOTE_CACHE")
