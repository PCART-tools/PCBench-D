def _nanmedian(arr1d):  # This only works on 1d arrays
    """Private function for rank a arrays. Compute the median ignoring Nan.

    Parameters
    ----------
    arr1d : ndarray
        Input array, of rank 1.

    Results
    -------
    m : float
        The median.
    """
    cond = ~np.isnan(arr1d)
    x = np.compress(cond, arr1d, axis=-1)
    if x.size == 0:
        return np.nan
    return np.median(x, overwrite_input=True)
