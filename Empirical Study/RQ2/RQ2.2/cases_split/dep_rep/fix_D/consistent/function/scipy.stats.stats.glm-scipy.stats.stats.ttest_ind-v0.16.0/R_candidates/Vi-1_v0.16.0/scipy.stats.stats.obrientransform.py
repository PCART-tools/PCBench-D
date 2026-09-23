def obrientransform(*args):
    """
    Computes the O'Brien transform on input data (any number of arrays).

    Used to test for homogeneity of variance prior to running one-way stats.
    Each array in ``*args`` is one level of a factor.
    If `f_oneway` is run on the transformed data and found significant,
    the variances are unequal.  From Maxwell and Delaney [1]_, p.112.

    Parameters
    ----------
    args : tuple of array_like
        Any number of arrays.

    Returns
    -------
    obrientransform : ndarray
        Transformed data for use in an ANOVA.  The first dimension
        of the result corresponds to the sequence of transformed
        arrays.  If the arrays given are all 1-D of the same length,
        the return value is a 2-D array; otherwise it is a 1-D array
        of type object, with each element being an ndarray.

    References
    ----------
    .. [1] S. E. Maxwell and H. D. Delaney, "Designing Experiments and
           Analyzing Data: A Model Comparison Perspective", Wadsworth, 1990.

    Examples
    --------
    We'll test the following data sets for differences in their variance.

    >>> x = [10, 11, 13, 9, 7, 12, 12, 9, 10]
    >>> y = [13, 21, 5, 10, 8, 14, 10, 12, 7, 15]

    Apply the O'Brien transform to the data.

    >>> from scipy.stats import obrientransform
    >>> tx, ty = obrientransform(x, y)

    Use `scipy.stats.f_oneway` to apply a one-way ANOVA test to the
    transformed data.

    >>> from scipy.stats import f_oneway
    >>> F, p = f_oneway(tx, ty)
    >>> p
    0.1314139477040335

    If we require that ``p < 0.05`` for significance, we cannot conclude
    that the variances are different.
    """
    TINY = np.sqrt(np.finfo(float).eps)

    # `arrays` will hold the transformed arguments.
    arrays = []

    for arg in args:
        a = np.asarray(arg)
        n = len(a)
        mu = np.mean(a)
        sq = (a - mu)**2
        sumsq = sq.sum()

        # The O'Brien transform.
        t = ((n - 1.5) * n * sq - 0.5 * sumsq) / ((n - 1) * (n - 2))

        # Check that the mean of the transformed data is equal to the
        # original variance.
        var = sumsq / (n - 1)
        if abs(var - np.mean(t)) > TINY:
            raise ValueError('Lack of convergence in obrientransform.')

        arrays.append(t)

    # If the arrays are not all the same shape, calling np.array(arrays)
    # creates a 1-D array with dtype `object` in numpy 1.6+. In numpy
    # 1.5.x, it raises an exception.  To work around this, we explicitly
    # set the dtype to `object` when the arrays are not all the same shape.
    if len(arrays) < 2 or all(x.shape == arrays[0].shape for x in arrays[1:]):
        dt = None
    else:
        dt = object
    return np.array(arrays, dtype=dt)
