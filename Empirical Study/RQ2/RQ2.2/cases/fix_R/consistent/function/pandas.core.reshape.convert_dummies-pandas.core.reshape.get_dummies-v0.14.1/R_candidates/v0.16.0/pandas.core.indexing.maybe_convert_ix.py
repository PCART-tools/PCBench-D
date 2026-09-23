def maybe_convert_ix(*args):
    """
    We likely want to take the cross-product
    """

    ixify = True
    for arg in args:
        if not isinstance(arg, (np.ndarray, list, ABCSeries)):
            ixify = False

    if ixify:
        return np.ix_(*args)
    else:
        return args
