@functools.lru_cache(None)
def fast_random_decomps() -> dict[Any, Callable[..., Any]]:
    return {**decompositions, **extra_random_decomps}
