def chisqprob(chisq, df):
    """
    Probability value (1-tail) for the Chi^2 probability distribution.

    Broadcasting rules apply.

    Parameters
    ----------
    chisq : array_like or float > 0

    df : array_like or float, probably int >= 1

    Returns
    -------
    chisqprob : ndarray
        The area from `chisq` to infinity under the Chi^2 probability
        distribution with degrees of freedom `df`.

    """
    return special.chdtrc(df, chisq)
