def is_bool_dtype(arr_or_dtype) -> bool:
    """
    Check whether the provided array or dtype is of a boolean dtype.

    Parameters
    ----------
    arr_or_dtype : array-like
        The array or dtype to check.

    Returns
    -------
    boolean
        Whether or not the array or dtype is of a boolean dtype.

    Notes
    -----
    An ExtensionArray is considered boolean when the ``_is_boolean``
    attribute is set to True.

    Examples
    --------
    >>> is_bool_dtype(str)
    False
    >>> is_bool_dtype(int)
    False
    >>> is_bool_dtype(bool)
    True
    >>> is_bool_dtype(np.bool_)
    True
    >>> is_bool_dtype(np.array(['a', 'b']))
    False
    >>> is_bool_dtype(pd.Series([1, 2]))
    False
    >>> is_bool_dtype(np.array([True, False]))
    True
    >>> is_bool_dtype(pd.Categorical([True, False]))
    True
    >>> is_bool_dtype(pd.arrays.SparseArray([True, False]))
    True
    """
    if arr_or_dtype is None:
        return False
    try:
        dtype = _get_dtype(arr_or_dtype)
    except TypeError:
        return False

    if isinstance(arr_or_dtype, CategoricalDtype):
        arr_or_dtype = arr_or_dtype.categories
        # now we use the special definition for Index

    if isinstance(arr_or_dtype, ABCIndexClass):

        # TODO(jreback)
        # we don't have a boolean Index class
        # so its object, we need to infer to
        # guess this
        return arr_or_dtype.is_object and arr_or_dtype.inferred_type == "boolean"
    elif is_extension_array_dtype(arr_or_dtype):
        dtype = getattr(arr_or_dtype, "dtype", arr_or_dtype)
        return dtype._is_boolean

    return issubclass(dtype.type, np.bool_)
