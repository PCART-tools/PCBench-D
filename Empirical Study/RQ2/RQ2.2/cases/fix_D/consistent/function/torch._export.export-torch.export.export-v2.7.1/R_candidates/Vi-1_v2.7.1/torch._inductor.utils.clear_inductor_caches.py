def clear_inductor_caches() -> None:
    """
    Clear all registered caches.
    """
    for obj in _registered_caches:
        obj.cache_clear()
