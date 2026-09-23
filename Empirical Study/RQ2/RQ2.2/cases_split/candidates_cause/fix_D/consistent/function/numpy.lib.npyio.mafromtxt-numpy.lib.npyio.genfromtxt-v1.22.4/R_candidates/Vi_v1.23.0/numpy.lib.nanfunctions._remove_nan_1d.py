def _remove_nan_1d(arr1d, overwrite_input=False):
    """
    Equivalent to arr1d[~arr1d.isnan()], but in a different order

    Presumably faster as it incurs fewer copies

    Parameters
    ----------
    arr1d : ndarray
        Array to remove nans from
    overwrite_input : bool
        True if `arr1d` can be modified in place

    Returns
    -------
    res : ndarray
        Array with nan elements removed
    overwrite_input : bool
        True if `res` can be modified in place, given the constraint on the
        input
    """
    if arr1d.dtype == object:
        # object arrays do not support `isnan` (gh-9009), so make a guess
        c = np.not_equal(arr1d, arr1d, dtype=bool)
    else:
        c = np.isnan(arr1d)

    s = np.nonzero(c)[0]
    if s.size == arr1d.size:
        warnings.warn("All-NaN slice encountered", RuntimeWarning,
                      stacklevel=5)
        return arr1d[:0], True
    elif s.size == 0:
        return arr1d, overwrite_input
    else:
        if not overwrite_input:
            arr1d = arr1d.copy()
        # select non-nans at end of array
        enonan = arr1d[-s.size:][~c[-s.size:]]
        # fill nans in beginning of array with non-nans of end
        arr1d[s[:enonan.size]] = enonan

        return arr1d[:-s.size], True
