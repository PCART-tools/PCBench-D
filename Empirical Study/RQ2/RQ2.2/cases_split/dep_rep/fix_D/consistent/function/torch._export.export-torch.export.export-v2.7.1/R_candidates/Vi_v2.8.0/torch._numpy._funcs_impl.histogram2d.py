def histogram2d(
    x,
    y,
    bins=10,
    range: Optional[ArrayLike] = None,
    normed=None,
    weights: Optional[ArrayLike] = None,
    density=None,
):
    # vendored from https://github.com/numpy/numpy/blob/v1.24.0/numpy/lib/twodim_base.py#L655-L821
    if len(x) != len(y):
        raise ValueError("x and y must have the same length.")

    try:
        N = len(bins)
    except TypeError:
        N = 1

    if N != 1 and N != 2:
        bins = [bins, bins]

    h, e = histogramdd((x, y), bins, range, normed, weights, density)

    return h, e[0], e[1]
