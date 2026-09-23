def maybe_cast_result_dtype(dtype: DtypeObj, how: str) -> DtypeObj:
    """
    Get the desired dtype of a result based on the
    input dtype and how it was computed.

    Parameters
    ----------
    dtype : DtypeObj
        Input dtype.
    how : str
        How the result was computed.

    Returns
    -------
    DtypeObj
        The desired dtype of the result.
    """
    from pandas.core.arrays.boolean import BooleanDtype
    from pandas.core.arrays.integer import Int64Dtype

    if how in ["add", "cumsum", "sum"] and (dtype == np.dtype(bool)):
        return np.dtype(np.int64)
    elif how in ["add", "cumsum", "sum"] and isinstance(dtype, BooleanDtype):
        return Int64Dtype()
    return dtype
