def _check_for_numpy(obj: Any) -> bool:
    return _NUMPY_AVAILABLE and _might_be(cast(Hashable, type(obj)), "numpy")
