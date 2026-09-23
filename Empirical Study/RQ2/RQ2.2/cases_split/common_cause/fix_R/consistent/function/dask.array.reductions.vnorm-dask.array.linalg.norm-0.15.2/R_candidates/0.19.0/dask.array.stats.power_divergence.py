@doc_wraps(scipy.stats.power_divergence)
def power_divergence(f_obs, f_exp=None, ddof=0, axis=0, lambda_=None):

    if isinstance(lambda_, str):
        # TODO: public api
        if lambda_ not in scipy.stats.stats._power_div_lambda_names:
            names = repr(list(scipy.stats.stats._power_div_lambda_names.keys()))[1:-1]
            raise ValueError("invalid string for lambda_: {0!r}.  Valid strings "
                             "are {1}".format(lambda_, names))
        lambda_ = scipy.stats.stats._power_div_lambda_names[lambda_]
    elif lambda_ is None:
        lambda_ = 1

    if f_exp is not None:
        # f_exp = np.atleast_1d(np.asanyarray(f_exp))
        pass
    else:
        f_exp = f_obs.mean(axis=axis, keepdims=True)

    # `terms` is the array of terms that are summed along `axis` to create
    # the test statistic.  We use some specialized code for a few special
    # cases of lambda_.
    if lambda_ == 1:
        # Pearson's chi-squared statistic
        terms = (f_obs - f_exp)**2 / f_exp
    elif lambda_ == 0:
        # Log-likelihood ratio (i.e. G-test)
        terms = 2.0 * _xlogy(f_obs, f_obs / f_exp)
    elif lambda_ == -1:
        # Modified log-likelihood ratio
        terms = 2.0 * _xlogy(f_exp, f_exp / f_obs)
    else:
        # General Cressie-Read power divergence.
        terms = f_obs * ((f_obs / f_exp)**lambda_ - 1)
        terms /= 0.5 * lambda_ * (lambda_ + 1)

    stat = terms.sum(axis=axis)

    num_obs = _count(terms, axis=axis)
    # ddof = asarray(ddof)
    p = delayed(distributions.chi2.sf)(stat, num_obs - 1 - ddof)

    return delayed(Power_divergenceResult, nout=2)(stat, p)
