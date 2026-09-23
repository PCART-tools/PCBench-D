def _factor_indexer(shape, labels):
    """
    given a tuple of shape and a list of Categorical labels, return the
    expanded label indexer
    """
    mult = np.array(shape)[::-1].cumprod()[::-1]
    return com._ensure_platform_int(
        np.sum(np.array(labels).T * np.append(mult, [1]), axis=1).T)
