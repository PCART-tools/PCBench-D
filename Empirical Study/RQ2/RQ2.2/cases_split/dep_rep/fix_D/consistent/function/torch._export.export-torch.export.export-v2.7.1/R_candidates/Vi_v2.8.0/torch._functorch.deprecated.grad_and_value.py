def grad_and_value(
    func: Callable, argnums: argnums_t = 0, has_aux: bool = False
) -> Callable:
    warn_deprecated("grad_and_value")
    return apis.grad_and_value(func, argnums, has_aux)
