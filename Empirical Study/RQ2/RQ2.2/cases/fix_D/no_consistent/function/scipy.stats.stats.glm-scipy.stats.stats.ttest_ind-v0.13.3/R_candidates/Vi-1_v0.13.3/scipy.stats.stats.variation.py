def variation(a, axis=0):
    """
    Computes the coefficient of variation, the ratio of the biased standard
    deviation to the mean.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or None
        Axis along which to calculate the coefficient of variation.

    References
    ----------
    .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.

    """
    a, axis = _chk_asarray(a, axis)
    return a.std(axis)/a.mean(axis)
