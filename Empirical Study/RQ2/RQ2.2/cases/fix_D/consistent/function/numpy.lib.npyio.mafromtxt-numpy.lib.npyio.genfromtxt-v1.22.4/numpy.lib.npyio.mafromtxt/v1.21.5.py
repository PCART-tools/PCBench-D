def mafromtxt(fname, **kwargs):
    """
    Load ASCII data stored in a text file and return a masked array.

    .. deprecated:: 1.17
        np.mafromtxt is a deprecated alias of `genfromtxt` which
        overwrites the ``usemask`` argument with `True` even when
        explicitly called as ``mafromtxt(..., usemask=False)``.
        Use `genfromtxt` instead.

    Parameters
    ----------
    fname, kwargs : For a description of input parameters, see `genfromtxt`.

    See Also
    --------
    numpy.genfromtxt : generic function to load ASCII data.

    """
    kwargs['usemask'] = True
    # Numpy 1.17
    warnings.warn(
        "np.mafromtxt is a deprecated alias of np.genfromtxt, "
        "prefer the latter.",
        DeprecationWarning, stacklevel=2)
    return genfromtxt(fname, **kwargs)
