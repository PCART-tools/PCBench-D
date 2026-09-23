def ppcc_max(x, brack=(0.0,1.0), dist='tukeylambda'):
    """Returns the shape parameter that maximizes the probability plot
    correlation coefficient for the given data to a one-parameter
    family of distributions.

    See also ppcc_plot
    """
    try:
        ppf_func = eval('distributions.%s.ppf' % dist)
    except AttributeError:
        raise ValueError("%s is not a valid distribution with a ppf." % dist)
    """
    res = inspect.getargspec(ppf_func)
    if not ('loc' == res[0][-2] and 'scale' == res[0][-1] and \
            0.0==res[-1][-2] and 1.0==res[-1][-1]):
        raise ValueError("Function has does not have default location "
              "and scale parameters\n  that are 0.0 and 1.0 respectively.")
    if (1 < len(res[0])-len(res[-1])-1) or \
       (1 > len(res[0])-3):
        raise ValueError("Must be a one-parameter family.")
    """
    N = len(x)
    # compute uniform median statistics
    Ui = zeros(N)*1.0
    Ui[-1] = 0.5**(1.0/N)
    Ui[0] = 1-Ui[-1]
    i = arange(2,N)
    Ui[1:-1] = (i-0.3175)/(N+0.365)
    osr = sort(x)
    # this function computes the x-axis values of the probability plot
    #  and computes a linear regression (including the correlation)
    #  and returns 1-r so that a minimization function maximizes the
    #  correlation

    def tempfunc(shape, mi, yvals, func):
        xvals = func(mi, shape)
        r, prob = stats.pearsonr(xvals, yvals)
        return 1-r
    return optimize.brent(tempfunc, brack=brack, args=(Ui, osr, ppf_func))
