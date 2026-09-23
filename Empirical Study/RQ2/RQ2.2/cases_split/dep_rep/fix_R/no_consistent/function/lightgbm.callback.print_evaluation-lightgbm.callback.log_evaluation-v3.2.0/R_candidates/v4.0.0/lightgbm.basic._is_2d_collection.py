def _is_2d_collection(data: Any) -> bool:
    """Check whether data is a 2-D collection."""
    return (
        _is_numpy_2d_array(data)
        or _is_2d_list(data)
        or isinstance(data, pd_DataFrame)
    )
