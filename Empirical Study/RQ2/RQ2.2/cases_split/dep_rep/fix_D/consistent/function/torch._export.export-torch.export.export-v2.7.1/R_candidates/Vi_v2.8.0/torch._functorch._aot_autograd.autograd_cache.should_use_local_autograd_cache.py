def should_use_local_autograd_cache():
    if torch._inductor.config.force_disable_caches:
        return False
    return config.enable_autograd_cache
