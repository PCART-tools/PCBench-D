@functools.lru_cache(None)
def get_pad_cache() -> torch._inductor.codecache.LocalCache:
    return torch._inductor.codecache.LocalCache()
