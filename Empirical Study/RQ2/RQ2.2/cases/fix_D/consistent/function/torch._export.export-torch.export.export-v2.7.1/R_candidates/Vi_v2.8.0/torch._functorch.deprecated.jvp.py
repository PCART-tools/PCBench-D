def jvp(
    func: Callable,
    primals: Any,
    tangents: Any,
    *,
    strict: bool = False,
    has_aux: bool = False,
):
    warn_deprecated("jvp")
    return _impl.jvp(func, primals, tangents, strict=strict, has_aux=has_aux)
