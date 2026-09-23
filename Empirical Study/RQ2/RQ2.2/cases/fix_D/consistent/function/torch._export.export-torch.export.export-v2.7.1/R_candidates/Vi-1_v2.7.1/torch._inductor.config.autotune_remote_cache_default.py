def autotune_remote_cache_default() -> Optional[bool]:
    return get_tristate_env("TORCHINDUCTOR_AUTOTUNE_REMOTE_CACHE")
