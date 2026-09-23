def _data_to_2d_numpy(data: Any, dtype: type = np.float32, name: str = 'list') -> np.ndarray:
    """Convert data to numpy 2-D array."""
    if _is_numpy_2d_array(data):
        return cast_numpy_array_to_dtype(data, dtype)
    if _is_2d_list(data):
        return np.array(data, dtype=dtype)
    if isinstance(data, pd_DataFrame):
        if _get_bad_pandas_dtypes(data.dtypes):
            raise ValueError('DataFrame.dtypes must be int, float or bool')
        return cast_numpy_array_to_dtype(data.values, dtype)
    raise TypeError(f"Wrong type({type(data).__name__}) for {name}.\n"
                    "It should be list of lists, numpy 2-D array or pandas DataFrame")
