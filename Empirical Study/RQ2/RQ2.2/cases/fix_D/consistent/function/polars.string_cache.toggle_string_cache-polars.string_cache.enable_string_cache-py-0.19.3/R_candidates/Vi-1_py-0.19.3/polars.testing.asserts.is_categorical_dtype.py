def is_categorical_dtype(data_type: Any) -> bool:
    """Check if the input is a polars Categorical dtype."""
    return (
        type(data_type) is DataTypeClass
        and issubclass(data_type, Categorical)
        or isinstance(data_type, Categorical)
    )
