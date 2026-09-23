def jacfwd(
    func: Callable,
    argnums: argnums_t = 0,
    has_aux: bool = False,
    *,
    randomness: str = "error",
):
    warn_deprecated("jacfwd")
    return _impl.jacfwd(func, argnums, has_aux, randomness=randomness)
