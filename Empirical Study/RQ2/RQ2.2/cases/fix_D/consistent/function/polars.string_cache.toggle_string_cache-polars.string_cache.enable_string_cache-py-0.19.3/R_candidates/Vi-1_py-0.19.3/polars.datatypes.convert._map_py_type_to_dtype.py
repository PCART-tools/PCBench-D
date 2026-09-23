@functools.lru_cache(16)
def _map_py_type_to_dtype(
    python_dtype: PythonDataType | type[object],
) -> PolarsDataType:
    """Convert Python data type to Polars data type."""
    if python_dtype is float:
        return Float64
    if python_dtype is int:
        return Int64
    if python_dtype is str:
        return Utf8
    if python_dtype is bool:
        return Boolean
    if issubclass(python_dtype, datetime):
        # `datetime` is a subclass of `date`,
        # so need to check `datetime` first
        return Datetime("us")
    if issubclass(python_dtype, date):
        return Date
    if python_dtype is timedelta:
        return Duration("us")
    if python_dtype is time:
        return Time
    if python_dtype is list:
        return List
    if python_dtype is tuple:
        return List
    if python_dtype is PyDecimal:
        return Decimal
    if python_dtype is bytes:
        return Binary
    if python_dtype is object:
        return Object
    if python_dtype is None.__class__:
        return Null

    # cover generic typing aliases, such as 'list[str]'
    if hasattr(python_dtype, "__origin__") and hasattr(python_dtype, "__args__"):
        base_type = python_dtype.__origin__
        if base_type is not None:
            dtype = _map_py_type_to_dtype(base_type)
            nested = python_dtype.__args__
            if len(nested) == 1:
                nested = nested[0]
            return (
                dtype
                if nested is None
                else dtype(_map_py_type_to_dtype(nested))  # type: ignore[operator]
            )

    raise TypeError("invalid type")
