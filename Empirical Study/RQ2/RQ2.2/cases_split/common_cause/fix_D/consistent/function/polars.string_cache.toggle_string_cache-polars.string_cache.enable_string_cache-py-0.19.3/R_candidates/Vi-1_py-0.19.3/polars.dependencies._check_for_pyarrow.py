def _check_for_pyarrow(obj: Any) -> bool:
    return _PYARROW_AVAILABLE and _might_be(cast(Hashable, type(obj)), "pyarrow")
