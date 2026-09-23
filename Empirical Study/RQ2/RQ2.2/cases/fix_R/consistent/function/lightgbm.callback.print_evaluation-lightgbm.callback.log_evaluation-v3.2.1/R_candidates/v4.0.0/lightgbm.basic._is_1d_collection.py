def _is_1d_collection(data: Any) -> bool:
    """Check whether data is a 1-D collection."""
    return (
        _is_numpy_1d_array(data)
        or _is_numpy_column_array(data)
        or _is_1d_list(data)
        or isinstance(data, pd_Series)
    )
