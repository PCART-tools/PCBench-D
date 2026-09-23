def find_result_type(left: ArrayLike, right: Any) -> DtypeObj:
    """
    Find the type/dtype for a the result of an operation between these objects.

    This is similar to find_common_type, but looks at the objects instead
    of just their dtypes. This can be useful in particular when one of the
    objects does not have a `dtype`.

    Parameters
    ----------
    left : np.ndarray or ExtensionArray
    right : Any

    Returns
    -------
    np.dtype or ExtensionDtype

    See also
    --------
    find_common_type
    numpy.result_type
    """
    new_dtype: DtypeObj

    if (
        isinstance(left, np.ndarray)
        and left.dtype.kind in ["i", "u", "c"]
        and (lib.is_integer(right) or lib.is_float(right))
    ):
        # e.g. with int8 dtype and right=512, we want to end up with
        # np.int16, whereas infer_dtype_from(512) gives np.int64,
        #  which will make us upcast too far.
        if lib.is_float(right) and right.is_integer() and left.dtype.kind != "f":
            right = int(right)

        new_dtype = np.result_type(left, right)

    elif is_valid_na_for_dtype(right, left.dtype):
        # e.g. IntervalDtype[int] and None/np.nan
        new_dtype = ensure_dtype_can_hold_na(left.dtype)

    else:
        dtype, _ = infer_dtype_from(right, pandas_dtype=True)

        new_dtype = find_common_type([left.dtype, dtype])

    return new_dtype
