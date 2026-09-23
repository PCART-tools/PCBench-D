def jacrev(
    func: Callable,
    argnums: Union[int, tuple[int]] = 0,
    *,
    has_aux=False,
    chunk_size: Optional[int] = None,
    _preallocate_and_copy=False,
):
    warn_deprecated("jacrev")
    return _impl.jacrev(
        func,
        argnums,
        has_aux=has_aux,
        chunk_size=chunk_size,
        _preallocate_and_copy=_preallocate_and_copy,
    )
