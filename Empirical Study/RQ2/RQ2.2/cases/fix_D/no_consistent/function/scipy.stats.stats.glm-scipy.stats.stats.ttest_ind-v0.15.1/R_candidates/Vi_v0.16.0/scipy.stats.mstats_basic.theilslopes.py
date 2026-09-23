def theilslopes(y, x=None, alpha=0.95):
    y = ma.asarray(y).flatten()
    if x is None:
        x = ma.arange(len(y), dtype=float)
    else:
        x = ma.asarray(x).flatten()
        if len(x) != len(y):
            raise ValueError("Incompatible lengths ! (%s<>%s)" % (len(y),len(x)))

    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    y._mask = x._mask = m
    # Disregard any masked elements of x or y
    y = y.compressed()
    x = x.compressed().astype(float)
    # We now have unmasked arrays so can use `stats.theilslopes`
    return stats.theilslopes(y, x, alpha=alpha)
