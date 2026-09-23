def f_value(ER, EF, dfR, dfF):
    """
    Returns an F-statistic for a restricted vs. unrestricted model.

    Parameters
    ----------
    ER : float
         `ER` is the sum of squared residuals for the restricted model
          or null hypothesis

    EF : float
         `EF` is the sum of squared residuals for the unrestricted model
          or alternate hypothesis

    dfR : int
          `dfR` is the degrees of freedom in the restricted model

    dfF : int
          `dfF` is the degrees of freedom in the unrestricted model

    Returns
    -------
    F-statistic : float

    """
    return ((ER-EF)/float(dfR-dfF) / (EF/float(dfF)))
