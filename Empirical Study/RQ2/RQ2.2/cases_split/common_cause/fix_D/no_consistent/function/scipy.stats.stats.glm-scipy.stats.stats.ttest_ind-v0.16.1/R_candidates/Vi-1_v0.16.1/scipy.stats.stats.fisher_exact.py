def fisher_exact(table, alternative='two-sided'):
    """Performs a Fisher exact test on a 2x2 contingency table.

    Parameters
    ----------
    table : array_like of ints
        A 2x2 contingency table.  Elements should be non-negative integers.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Which alternative hypothesis to the null hypothesis the test uses.
        Default is 'two-sided'.

    Returns
    -------
    oddsratio : float
        This is prior odds ratio and not a posterior estimate.
    p_value : float
        P-value, the probability of obtaining a distribution at least as
        extreme as the one that was actually observed, assuming that the
        null hypothesis is true.

    See Also
    --------
    chi2_contingency : Chi-square test of independence of variables in a
        contingency table.

    Notes
    -----
    The calculated odds ratio is different from the one R uses. This scipy
    implementation returns the (more common) "unconditional Maximum
    Likelihood Estimate", while R uses the "conditional Maximum Likelihood
    Estimate".

    For tables with large numbers, the (inexact) chi-square test implemented
    in the function `chi2_contingency` can also be used.

    Examples
    --------
    Say we spend a few days counting whales and sharks in the Atlantic and
    Indian oceans. In the Atlantic ocean we find 8 whales and 1 shark, in the
    Indian ocean 2 whales and 5 sharks. Then our contingency table is::

                Atlantic  Indian
        whales     8        2
        sharks     1        5

    We use this table to find the p-value:

    >>> import scipy.stats as stats
    >>> oddsratio, pvalue = stats.fisher_exact([[8, 2], [1, 5]])
    >>> pvalue
    0.0349...

    The probability that we would observe this or an even more imbalanced ratio
    by chance is about 3.5%.  A commonly used significance level is 5%--if we
    adopt that, we can therefore conclude that our observed imbalance is
    statistically significant; whales prefer the Atlantic while sharks prefer
    the Indian ocean.

    """
    hypergeom = distributions.hypergeom
    c = np.asarray(table, dtype=np.int64)  # int32 is not enough for the algorithm
    if not c.shape == (2, 2):
        raise ValueError("The input `table` must be of shape (2, 2).")

    if np.any(c < 0):
        raise ValueError("All values in `table` must be nonnegative.")

    if 0 in c.sum(axis=0) or 0 in c.sum(axis=1):
        # If both values in a row or column are zero, the p-value is 1 and
        # the odds ratio is NaN.
        return np.nan, 1.0

    if c[1,0] > 0 and c[0,1] > 0:
        oddsratio = c[0,0] * c[1,1] / float(c[1,0] * c[0,1])
    else:
        oddsratio = np.inf

    n1 = c[0,0] + c[0,1]
    n2 = c[1,0] + c[1,1]
    n = c[0,0] + c[1,0]

    def binary_search(n, n1, n2, side):
        """Binary search for where to begin lower/upper halves in two-sided
        test.
        """
        if side == "upper":
            minval = mode
            maxval = n
        else:
            minval = 0
            maxval = mode
        guess = -1
        while maxval - minval > 1:
            if maxval == minval + 1 and guess == minval:
                guess = maxval
            else:
                guess = (maxval + minval) // 2
            pguess = hypergeom.pmf(guess, n1 + n2, n1, n)
            if side == "upper":
                ng = guess - 1
            else:
                ng = guess + 1
            if pguess <= pexact < hypergeom.pmf(ng, n1 + n2, n1, n):
                break
            elif pguess < pexact:
                maxval = guess
            else:
                minval = guess
        if guess == -1:
            guess = minval
        if side == "upper":
            while guess > 0 and hypergeom.pmf(guess, n1 + n2, n1, n) < pexact * epsilon:
                guess -= 1
            while hypergeom.pmf(guess, n1 + n2, n1, n) > pexact / epsilon:
                guess += 1
        else:
            while hypergeom.pmf(guess, n1 + n2, n1, n) < pexact * epsilon:
                guess += 1
            while guess > 0 and hypergeom.pmf(guess, n1 + n2, n1, n) > pexact / epsilon:
                guess -= 1
        return guess

    if alternative == 'less':
        pvalue = hypergeom.cdf(c[0,0], n1 + n2, n1, n)
    elif alternative == 'greater':
        # Same formula as the 'less' case, but with the second column.
        pvalue = hypergeom.cdf(c[0,1], n1 + n2, n1, c[0,1] + c[1,1])
    elif alternative == 'two-sided':
        mode = int(float((n + 1) * (n1 + 1)) / (n1 + n2 + 2))
        pexact = hypergeom.pmf(c[0,0], n1 + n2, n1, n)
        pmode = hypergeom.pmf(mode, n1 + n2, n1, n)

        epsilon = 1 - 1e-4
        if np.abs(pexact - pmode) / np.maximum(pexact, pmode) <= 1 - epsilon:
            return oddsratio, 1.

        elif c[0,0] < mode:
            plower = hypergeom.cdf(c[0,0], n1 + n2, n1, n)
            if hypergeom.pmf(n, n1 + n2, n1, n) > pexact / epsilon:
                return oddsratio, plower

            guess = binary_search(n, n1, n2, "upper")
            pvalue = plower + hypergeom.sf(guess - 1, n1 + n2, n1, n)
        else:
            pupper = hypergeom.sf(c[0,0] - 1, n1 + n2, n1, n)
            if hypergeom.pmf(0, n1 + n2, n1, n) > pexact / epsilon:
                return oddsratio, pupper

            guess = binary_search(n, n1, n2, "lower")
            pvalue = pupper + hypergeom.cdf(guess, n1 + n2, n1, n)
    else:
        msg = "`alternative` should be one of {'two-sided', 'less', 'greater'}"
        raise ValueError(msg)

    if pvalue > 1.0:
        pvalue = 1.0

    return oddsratio, pvalue
