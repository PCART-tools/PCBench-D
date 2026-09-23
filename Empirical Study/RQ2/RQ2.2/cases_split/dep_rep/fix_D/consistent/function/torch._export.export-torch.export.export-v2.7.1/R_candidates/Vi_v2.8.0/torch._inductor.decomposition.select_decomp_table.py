def select_decomp_table() -> dict[Any, Callable[..., Any]]:
    """decomps can change based on config"""
    if config.fallback_random:
        return decompositions
    return fast_random_decomps()
