def construct_1d_ndarray_preserving_na(values, dtype=None, copy: bool = False):
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
    subarr = np.array(values, dtype=dtype, copy=copy)

    if dtype is not None and dtype.kind in ("U", "S"):
        # GH-21083
        # We can't just return np.array(subarr, dtype='str') since
        # NumPy will convert the non-string objects into strings
        # Including NA values. Se we have to go
        # string -> object -> update NA, which requires an
        # additional pass over the data.
        na_values = isna(values)
        subarr2 = subarr.astype(object)
        subarr2[na_values] = np.asarray(values, dtype=object)[na_values]
        subarr = subarr2

    return subarr
