def trim1(a, proportiontocut, tail='right'):
    """
    Slices off a proportion of items from ONE end of the passed array
    distribution.

    If `proportiontocut` = 0.1, slices off 'leftmost' or 'rightmost'
    10% of scores.  Slices off LESS if proportion results in a non-integer
    slice index (i.e., conservatively slices off `proportiontocut` ).

    Parameters
    ----------
    a : array_like
        Input array
    proportiontocut : float
        Fraction to cut off of 'left' or 'right' of distribution
    tail : {'left', 'right'}, optional
        Defaults to 'right'.

    Returns
    -------
    trim1 : ndarray
        Trimmed version of array `a`

    """
    a = asarray(a)
    if tail.lower() == 'right':
        lowercut = 0
        uppercut = len(a) - int(proportiontocut*len(a))
    elif tail.lower() == 'left':
        lowercut = int(proportiontocut*len(a))
        uppercut = len(a)

    return a[lowercut:uppercut]
