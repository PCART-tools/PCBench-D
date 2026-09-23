def trim1(a, proportiontocut, tail='right', axis=0):
    """
    Slices off a proportion from ONE end of the passed array distribution.

    If `proportiontocut` = 0.1, slices off 'leftmost' or 'rightmost'
    10% of scores. The lowest or highest values are trimmed (depending on
    the tail).
    Slices off less if proportion results in a non-integer slice index
    (i.e., conservatively slices off `proportiontocut` ).

    Parameters
    ----------
    a : array_like
        Input array
    proportiontocut : float
        Fraction to cut off of 'left' or 'right' of distribution
    tail : {'left', 'right'}, optional
        Defaults to 'right'.
    axis : int or None, optional
        Axis along which to trim data. Default is 0. If None, compute over
        the whole array `a`.

    Returns
    -------
    trim1 : ndarray
        Trimmed version of array `a`. The order of the trimmed content is
        undefined.

    """
    a = np.asarray(a)
    if axis is None:
        a = a.ravel()
        axis = 0

    nobs = a.shape[axis]

    # avoid possible corner case
    if proportiontocut >= 1:
        return []

    if tail.lower() == 'right':
        lowercut = 0
        uppercut = nobs - int(proportiontocut * nobs)

    elif tail.lower() == 'left':
        lowercut = int(proportiontocut * nobs)
        uppercut = nobs

    # np.partition is preferred but it only exist in numpy 1.8.0 and higher,
    # in those cases we use np.sort
    try:
        atmp = np.partition(a, (lowercut, uppercut - 1), axis)
    except AttributeError:
        atmp = np.sort(a, axis)

    return atmp[lowercut:uppercut]
