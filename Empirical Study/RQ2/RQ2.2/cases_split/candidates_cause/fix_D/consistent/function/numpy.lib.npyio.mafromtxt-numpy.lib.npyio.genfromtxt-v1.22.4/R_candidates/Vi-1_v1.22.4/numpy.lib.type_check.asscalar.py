@array_function_dispatch(_asscalar_dispatcher)
def asscalar(a):
    """
    Convert an array of size 1 to its scalar equivalent.

    .. deprecated:: 1.16

        Deprecated, use `numpy.ndarray.item()` instead.

    Parameters
    ----------
    a : ndarray
        Input array of size 1.

    Returns
    -------
    out : scalar
        Scalar representation of `a`. The output data type is the same type
        returned by the input's `item` method.

    Examples
    --------
    >>> np.asscalar(np.array([24]))
    24
    """
    return a.item()
