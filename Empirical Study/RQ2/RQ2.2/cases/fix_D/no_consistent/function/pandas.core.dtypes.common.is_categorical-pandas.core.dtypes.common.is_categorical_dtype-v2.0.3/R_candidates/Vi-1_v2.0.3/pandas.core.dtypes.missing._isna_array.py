def _isna_array(values: ArrayLike, inf_as_na: bool = False):
    """
    Return an array indicating which values of the input array are NaN / NA.

    Parameters
    ----------
    obj: ndarray or ExtensionArray
        The input array whose elements are to be checked.
    inf_as_na: bool
        Whether or not to treat infinite values as NA.

    Returns
    -------
    array-like
        Array of boolean values denoting the NA status of each element.
    """
    dtype = values.dtype

    if not isinstance(values, np.ndarray):
        # i.e. ExtensionArray
        if inf_as_na and is_categorical_dtype(dtype):
            result = libmissing.isnaobj(values.to_numpy(), inf_as_na=inf_as_na)
        else:
            # error: Incompatible types in assignment (expression has type
            # "Union[ndarray[Any, Any], ExtensionArraySupportsAnyAll]", variable has
            # type "ndarray[Any, dtype[bool_]]")
            result = values.isna()  # type: ignore[assignment]
    elif is_string_or_object_np_dtype(values.dtype):
        result = _isna_string_dtype(values, inf_as_na=inf_as_na)
    elif needs_i8_conversion(dtype):
        # this is the NaT pattern
        result = values.view("i8") == iNaT
    else:
        if inf_as_na:
            result = ~np.isfinite(values)
        else:
            result = np.isnan(values)

    return result
