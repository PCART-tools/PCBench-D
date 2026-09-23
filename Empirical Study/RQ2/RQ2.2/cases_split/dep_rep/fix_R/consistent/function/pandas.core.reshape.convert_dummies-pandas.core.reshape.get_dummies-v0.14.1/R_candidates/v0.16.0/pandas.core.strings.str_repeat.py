def str_repeat(arr, repeats):
    """
    Duplicate each string in the array by indicated number of times

    Parameters
    ----------
    repeats : int or array
        Same value for all (int) or different value per (array)

    Returns
    -------
    repeated : array
    """
    if np.isscalar(repeats):
        def rep(x):
            try:
                return compat.binary_type.__mul__(x, repeats)
            except TypeError:
                return compat.text_type.__mul__(x, repeats)

        return _na_map(rep, arr)
    else:
        def rep(x, r):
            try:
                return compat.binary_type.__mul__(x, r)
            except TypeError:
                return compat.text_type.__mul__(x, r)

        repeats = np.asarray(repeats, dtype=object)
        result = lib.vec_binop(_values_from_object(arr), repeats, rep)
        return result
