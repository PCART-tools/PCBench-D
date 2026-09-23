def _transformList(l):
    ret = np.empty(len(l), dtype=np.object)
    for (i, arr) in enumerate(l):
        ret[i] = arr
    return ret
