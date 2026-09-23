def list_to_1d_numpy(data, dtype=np.float32, name='list'):
    """Convert data to numpy 1-D array."""
    if is_numpy_1d_array(data):
        return cast_numpy_array_to_dtype(data, dtype)
    elif is_numpy_column_array(data):
        _log_warning('Converting column-vector to 1d array')
        array = data.ravel()
        return cast_numpy_array_to_dtype(array, dtype)
    elif is_1d_list(data):
        return np.array(data, dtype=dtype, copy=False)
    elif isinstance(data, pd_Series):
        if _get_bad_pandas_dtypes([data.dtypes]):
            raise ValueError('Series.dtypes must be int, float or bool')
        return np.array(data, dtype=dtype, copy=False)  # SparseArray should be supported as well
    else:
        raise TypeError(f"Wrong type({type(data).__name__}) for {name}.\n"
                        "It should be list, numpy 1-D array or pandas Series")
