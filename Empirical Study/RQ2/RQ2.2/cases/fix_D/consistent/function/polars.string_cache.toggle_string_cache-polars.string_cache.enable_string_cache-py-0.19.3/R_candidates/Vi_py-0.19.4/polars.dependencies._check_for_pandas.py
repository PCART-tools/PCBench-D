def _check_for_pandas(obj: Any) -> bool:
    return _PANDAS_AVAILABLE and _might_be(cast(Hashable, type(obj)), "pandas")
