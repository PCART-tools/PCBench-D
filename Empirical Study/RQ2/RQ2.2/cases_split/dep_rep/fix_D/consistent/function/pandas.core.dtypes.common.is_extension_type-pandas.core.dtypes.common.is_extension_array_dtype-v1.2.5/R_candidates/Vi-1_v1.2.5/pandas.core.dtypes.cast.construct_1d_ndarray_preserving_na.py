def construct_1d_ndarray_preserving_na(
    values: Sequence, dtype: Optional[DtypeObj] = None, copy: bool = False
) -> np.ndarray:
    """
    Construct a new ndarray, coercing `values` to `dtype`, preserving NA.

    Parameters
    ----------
    values : Sequence
    dtype : numpy.dtype, optional
    copy : bool, default False
        Note that copies may still be made with ``copy=False`` if casting
        is required.

    Returns
    -------
    arr : ndarray[dtype]

    Examples
    --------
    >>> np.array([1.0, 2.0, None], dtype='str')
    array(['1.0', '2.0', 'None'], dtype='<U4')

    >>> construct_1d_ndarray_preserving_na([1.0, 2.0, None], dtype=np.dtype('str'))
    array(['1.0', '2.0', None], dtype=object)
    """

    if dtype is not None and dtype.kind == "U":
        subarr = lib.ensure_string_array(values, convert_na_value=False, copy=copy)
    else:
        subarr = np.array(values, dtype=dtype, copy=copy)

    return subarr
