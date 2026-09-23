def linregress(x, y=None):
    """
    Linear regression calculation

    Note that the non-masked version is used, and that this docstring is
    replaced by the non-masked docstring + some info on missing data.

    """
    if y is None:
        x = ma.array(x)
        if x.shape[0] == 2:
            x, y = x
        elif x.shape[1] == 2:
            x, y = x.T
        else:
            msg = ("If only `x` is given as input, it has to be of shape "
                   "(2, N) or (N, 2), provided shape was %s" % str(x.shape))
            raise ValueError(msg)
    else:
        x = ma.array(x)
        y = ma.array(y)

    x = x.flatten()
    y = y.flatten()

    m = ma.mask_or(ma.getmask(x), ma.getmask(y), shrink=False)
    if m is not nomask:
        x = ma.array(x, mask=m)
        y = ma.array(y, mask=m)
        if np.any(~m):
            slope, intercept, r, prob, sterrest = stats_linregress(x.data[~m],
                                                                   y.data[~m])
        else:
            # All data is masked
            return None, None, None, None, None
    else:
        slope, intercept, r, prob, sterrest = stats_linregress(x.data, y.data)

    return LinregressResult(slope, intercept, r, prob, sterrest)
