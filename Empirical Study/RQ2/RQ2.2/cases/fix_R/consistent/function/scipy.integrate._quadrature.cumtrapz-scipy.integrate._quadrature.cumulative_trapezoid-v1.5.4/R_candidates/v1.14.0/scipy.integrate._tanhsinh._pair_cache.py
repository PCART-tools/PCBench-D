def _pair_cache(k, h0):
    # Cache the abscissa-weight pairs up to a specified level.
    # Abscissae and weights of consecutive levels are concatenated.
    # `index` records the indices that correspond with each level:
    # `xjc[index[k]:index[k+1]` extracts the level `k` abscissae.
    if h0 != _pair_cache.h0:
        _pair_cache.xjc = np.empty(0)
        _pair_cache.wj = np.empty(0)
        _pair_cache.indices = [0]

    xjcs = [_pair_cache.xjc]
    wjs = [_pair_cache.wj]

    for i in range(len(_pair_cache.indices)-1, k + 1):
        xjc, wj = _compute_pair(i, h0)
        xjcs.append(xjc)
        wjs.append(wj)
        _pair_cache.indices.append(_pair_cache.indices[-1] + len(xjc))

    _pair_cache.xjc = np.concatenate(xjcs)
    _pair_cache.wj = np.concatenate(wjs)
    _pair_cache.h0 = h0
