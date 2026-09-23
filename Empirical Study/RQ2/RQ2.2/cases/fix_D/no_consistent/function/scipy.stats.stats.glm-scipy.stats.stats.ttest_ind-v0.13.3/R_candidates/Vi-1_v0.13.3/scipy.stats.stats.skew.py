def skew(a, axis=0, bias=True):
    """
    Computes the skewness of a data set.

    For normally distributed data, the skewness should be about 0. A skewness
    value > 0 means that there is more weight in the left tail of the
    distribution. The function `skewtest` can be used to determine if the
    skewness value is close enough to 0, statistically speaking.

    Parameters
    ----------
    a : ndarray
        data
    axis : int or None
        axis along which skewness is calculated
    bias : bool
        If False, then the calculations are corrected for statistical bias.

    Returns
    -------
    skewness : ndarray
        The skewness of values along an axis, returning 0 where all values are
        equal.

    References
    ----------
    [CRCProbStat2000]_ Section 2.2.24.1

    .. [CRCProbStat2000] Zwillinger, D. and Kokoska, S. (2000). CRC Standard
       Probability and Statistics Tables and Formulae. Chapman & Hall: New
       York. 2000.

    """
    a, axis = _chk_asarray(a,axis)
    n = a.shape[axis]
    m2 = moment(a, 2, axis)
    m3 = moment(a, 3, axis)
    zero = (m2 == 0)
    vals = np.where(zero, 0, m3 / m2**1.5)
    if not bias:
        can_correct = (n > 2) & (m2 > 0)
        if can_correct.any():
            m2 = np.extract(can_correct, m2)
            m3 = np.extract(can_correct, m3)
            nval = np.sqrt((n-1.0)*n)/(n-2.0)*m3/m2**1.5
            np.place(vals, can_correct, nval)
    if vals.ndim == 0:
        return vals.item()
    return vals
