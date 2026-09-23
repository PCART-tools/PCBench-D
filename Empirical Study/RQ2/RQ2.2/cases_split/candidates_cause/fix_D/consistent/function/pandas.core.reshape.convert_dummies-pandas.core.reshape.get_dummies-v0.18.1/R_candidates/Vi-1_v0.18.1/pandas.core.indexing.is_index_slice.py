def is_index_slice(obj):
    def _is_valid_index(x):
        return (is_integer(x) or is_float(x) and
                np.allclose(x, int(x), rtol=_eps, atol=0))

    def _crit(v):
        return v is None or _is_valid_index(v)

    both_none = obj.start is None and obj.stop is None

    return not both_none and (_crit(obj.start) and _crit(obj.stop))
