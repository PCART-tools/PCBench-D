def _is_allowed_numpy_dtype(dtype: type) -> bool:
    float128 = getattr(np, 'float128', type(None))
    return (
        issubclass(dtype, (np.integer, np.floating, np.bool_))
        and not issubclass(dtype, (np.timedelta64, float128))
    )
