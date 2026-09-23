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
    from pandas.core.arrays.floating import Float64Dtype
    from pandas.core.arrays.integer import Int64Dtype, _IntegerDtype

    if how in ["add", "cumsum", "sum", "prod"]:
        if dtype == np.dtype(bool):
            return np.dtype(np.int64)
        elif isinstance(dtype, (BooleanDtype, _IntegerDtype)):
            return Int64Dtype()
    elif how in ["mean", "median", "var"] and isinstance(
        dtype, (BooleanDtype, _IntegerDtype)
    ):
        return Float64Dtype()
    return dtype
