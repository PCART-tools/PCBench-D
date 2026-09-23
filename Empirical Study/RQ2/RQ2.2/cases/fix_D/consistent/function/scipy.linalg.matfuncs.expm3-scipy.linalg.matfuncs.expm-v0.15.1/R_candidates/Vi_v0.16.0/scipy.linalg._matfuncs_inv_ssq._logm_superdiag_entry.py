def _logm_superdiag_entry(l1, l2, t12):
    """
    Compute a superdiagonal entry of a matrix logarithm.

    This is Eq. (11.28) in [1]_.

    Parameters
    ----------
    l1 : complex
        A diagonal entry of the matrix.
    l2 : complex
        A diagonal entry of the matrix.
    t12 : complex
        A superdiagonal entry of the matrix.

    Returns
    -------
    f12 : complex
        A superdiagonal entry of the matrix logarithm.

    Notes
    -----
    Some amount of care has been taken to return a real number
    if all of the inputs are real.

    References
    ----------
    .. [1] Nicholas J. Higham (2008)
           "Functions of Matrices: Theory and Computation"
           ISBN 978-0-898716-46-7

    """
    if l1 == l2:
        f12 = t12 / l1
    elif abs(l1) < abs(l2) / 2 or abs(l2) < abs(l1) / 2:
        f12 = t12 * (np.log(l2) - np.log(l1)) / (l2 - l1)
    else:
        z = (l2 - l1) / (l2 + l1)
        ua = _unwindk(np.log(l2) - np.log(l1))
        ub = _unwindk(np.log(1+z) - np.log(1-z))
        u = ua + ub
        if u:
            f12 = t12 * (2*np.arctanh(z) + 2*np.pi*1j*(ua + ub)) / (l2 - l1)
        else:
            f12 = t12 * 2 * np.arctanh(z) / (l2 - l1)
    return f12
