def grad(func: Callable, argnums: argnums_t = 0, has_aux: bool = False) -> Callable:
    warn_deprecated("grad")
    return apis.grad(func, argnums, has_aux)
