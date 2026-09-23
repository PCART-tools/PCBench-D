def _isna_ndarraylike(obj, inf_as_na: bool = False):
    """
    Return an array indicating which values of the input array are NaN / NA.

    Parameters
    ----------
    obj: array-like
        The input array whose elements are to be checked.
    inf_as_na: bool
        Whether or not to treat infinite values as NA.

    Returns
    -------
    array-like
        Array of boolean values denoting the NA status of each element.
    """
    values = getattr(obj, "_values", obj)
    dtype = values.dtype

    if is_extension_array_dtype(dtype):
        if inf_as_na and is_categorical_dtype(dtype):
            result = libmissing.isnaobj_old(values.to_numpy())
        else:
            result = values.isna()
    elif is_string_dtype(dtype):
        result = _isna_string_dtype(values, dtype, inf_as_na=inf_as_na)
    elif needs_i8_conversion(dtype):
        # this is the NaT pattern
        result = values.view("i8") == iNaT
    else:
        if inf_as_na:
            result = ~np.isfinite(values)
        else:
            result = np.isnan(values)

    # box
    if isinstance(obj, ABCSeries):
        result = obj._constructor(result, index=obj.index, name=obj.name, copy=False)

    return result
