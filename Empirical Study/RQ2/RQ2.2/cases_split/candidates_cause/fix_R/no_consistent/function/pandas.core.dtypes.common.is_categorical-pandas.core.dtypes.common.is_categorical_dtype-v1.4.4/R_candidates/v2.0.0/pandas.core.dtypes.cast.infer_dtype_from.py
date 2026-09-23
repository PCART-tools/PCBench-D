def infer_dtype_from(val, pandas_dtype: bool = False) -> tuple[DtypeObj, Any]:
    """
    Interpret the dtype from a scalar or array.

    Parameters
    ----------
    val : object
    pandas_dtype : bool, default False
        whether to infer dtype including pandas extension types.
        If False, scalar/array belongs to pandas extension types is inferred as
        object
    """
    if not is_list_like(val):
        return infer_dtype_from_scalar(val, pandas_dtype=pandas_dtype)
    return infer_dtype_from_array(val, pandas_dtype=pandas_dtype)
