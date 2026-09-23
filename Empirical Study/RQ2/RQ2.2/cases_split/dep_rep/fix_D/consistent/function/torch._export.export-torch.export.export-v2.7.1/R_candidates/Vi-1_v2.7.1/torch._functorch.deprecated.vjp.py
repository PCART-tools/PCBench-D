def vjp(func: Callable, *primals, has_aux: bool = False):
    warn_deprecated("vjp")
    return _impl.vjp(func, *primals, has_aux=has_aux)
