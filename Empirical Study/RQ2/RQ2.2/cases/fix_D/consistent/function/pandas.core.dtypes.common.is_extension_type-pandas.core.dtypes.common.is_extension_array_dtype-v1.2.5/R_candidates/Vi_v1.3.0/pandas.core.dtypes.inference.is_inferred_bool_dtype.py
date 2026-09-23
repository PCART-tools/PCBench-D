def is_inferred_bool_dtype(arr: ArrayLike) -> bool:
    """
    Check if this is a ndarray[bool] or an ndarray[object] of bool objects.

    Parameters
    ----------
    arr : np.ndarray or ExtensionArray

    Returns
    -------
    bool

    Notes
    -----
    This does not include the special treatment is_bool_dtype uses for
    Categorical.
    """
    if not isinstance(arr, np.ndarray):
        return False

    dtype = arr.dtype
    if dtype == np.dtype(bool):
        return True
    elif dtype == np.dtype("object"):
        return lib.is_bool_array(arr.ravel("K"))
    return False
