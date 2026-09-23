@np.deprecate(message="stats.f_value_multivariate deprecated in scipy 0.17.0")
def f_value_multivariate(ER, EF, dfnum, dfden):
    """
    Returns a multivariate F-statistic.

    Parameters
    ----------
    ER : ndarray
        Error associated with the null hypothesis (the Restricted model).
        From a multivariate F calculation.
    EF : ndarray
        Error associated with the alternate hypothesis (the Full model)
        From a multivariate F calculation.
    dfnum : int
        Degrees of freedom the Restricted model.
    dfden : int
        Degrees of freedom associated with the Restricted model.

    Returns
    -------
    fstat : float
        The computed F-statistic.

    """
    if isinstance(ER, (int, float)):
        ER = array([[ER]])
    if isinstance(EF, (int, float)):
        EF = array([[EF]])
    n_um = (linalg.det(ER) - linalg.det(EF)) / float(dfnum)
    d_en = linalg.det(EF) / float(dfden)
    return n_um / d_en
