def linregress(*args):
    """
    Linear regression calculation

    Note that the non-masked version is used, and that this docstring is
    replaced by the non-masked docstring + some info on missing data.

    """
    if len(args) == 1:
        # Input is a single 2-D array containing x and y
        args = ma.array(args[0], copy=True)
        if len(args) == 2:
            x = args[0]
            y = args[1]
        else:
            x = args[:, 0]
            y = args[:, 1]
    else:
        # Input is two 1-D arrays
        x = ma.array(args[0]).flatten()
        y = ma.array(args[1]).flatten()

    m = ma.mask_or(ma.getmask(x), ma.getmask(y), shrink=False)
    if m is not nomask:
        x = ma.array(x, mask=m)
        y = ma.array(y, mask=m)
        if np.any(~m):
            slope, intercept, r, prob, sterrest = stats.linregress(x.data[~m],
                                                                   y.data[~m])
        else:
            # All data is masked
            return None, None, None, None, None
    else:
        slope, intercept, r, prob, sterrest = stats.linregress(x.data, y.data)

    return LinregressResult(slope, intercept, r, prob, sterrest)
