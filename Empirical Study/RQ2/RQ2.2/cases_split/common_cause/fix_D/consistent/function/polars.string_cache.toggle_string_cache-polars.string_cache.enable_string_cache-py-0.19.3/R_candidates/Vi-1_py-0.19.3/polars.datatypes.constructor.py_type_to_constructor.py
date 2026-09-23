def py_type_to_constructor(dtype: type[Any]) -> Callable[..., PySeries]:
    """Get the right PySeries constructor for the given Python dtype."""
    try:
        return _PY_TYPE_TO_CONSTRUCTOR[dtype]
    except KeyError:
        return PySeries.new_object
