def cache_decorator(func: Callable) -> CacheAttributes:
    return cast(CacheAttributes, func)
