@array_function_dispatch(_msort_dispatcher)
def msort(a):
    """
    Return a copy of an array sorted along the first axis.

    Parameters
    ----------
    a : array_like
        Array to be sorted.

    Returns
    -------
    sorted_array : ndarray
        Array of the same type and shape as `a`.

    See Also
    --------
    sort

    Notes
    -----
    ``np.msort(a)`` is equivalent to  ``np.sort(a, axis=0)``.

    """
    b = array(a, subok=True, copy=True)
    b.sort(0)
    return b
