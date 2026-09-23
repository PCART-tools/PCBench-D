def compare_medians_ms(group_1, group_2, axis=None):
    """
    Compares the medians from two independent groups along the given axis.

    The comparison is performed using the McKean-Schrader estimate of the
    standard error of the medians.

    Parameters
    ----------
    group_1 : array_like
        First dataset.
    group_2 : array_like
        Second dataset.
    axis : int, optional
        Axis along which the medians are estimated. If None, the arrays are
        flattened.  If `axis` is not None, then `group_1` and `group_2`
        should have the same shape.

    Returns
    -------
    compare_medians_ms : {float, ndarray}
        If `axis` is None, then returns a float, otherwise returns a 1-D
        ndarray of floats with a length equal to the length of `group_1`
        along `axis`.

    """
    (med_1, med_2) = (ma.median(group_1,axis=axis), ma.median(group_2,axis=axis))
    (std_1, std_2) = (mstats.stde_median(group_1, axis=axis),
                      mstats.stde_median(group_2, axis=axis))
    W = np.abs(med_1 - med_2) / ma.sqrt(std_1**2 + std_2**2)
    return 1 - norm.cdf(W)
