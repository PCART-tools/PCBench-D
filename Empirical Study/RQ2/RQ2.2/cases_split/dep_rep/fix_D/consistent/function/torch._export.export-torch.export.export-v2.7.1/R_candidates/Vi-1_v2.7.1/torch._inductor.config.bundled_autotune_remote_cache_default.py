def bundled_autotune_remote_cache_default() -> Optional[bool]:
    return get_tristate_env("TORCHINDUCTOR_BUNDLED_AUTOTUNE_REMOTE_CACHE")
