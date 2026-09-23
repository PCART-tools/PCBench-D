def ppcc_max(x, brack=(0.0, 1.0), dist='tukeylambda'):
    """Returns the shape parameter that maximizes the probability plot
    correlation coefficient for the given data to a one-parameter
    family of distributions.

    See also ppcc_plot
    """
    dist = _parse_dist_kw(dist)
    osm_uniform = _calc_uniform_order_statistic_medians(x)
    osr = sort(x)

    # this function computes the x-axis values of the probability plot
    #  and computes a linear regression (including the correlation)
    #  and returns 1-r so that a minimization function maximizes the
    #  correlation
    def tempfunc(shape, mi, yvals, func):
        xvals = func(mi, shape)
        r, prob = stats.pearsonr(xvals, yvals)
        return 1 - r

    return optimize.brent(tempfunc, brack=brack, args=(osm_uniform, osr, dist.ppf))
