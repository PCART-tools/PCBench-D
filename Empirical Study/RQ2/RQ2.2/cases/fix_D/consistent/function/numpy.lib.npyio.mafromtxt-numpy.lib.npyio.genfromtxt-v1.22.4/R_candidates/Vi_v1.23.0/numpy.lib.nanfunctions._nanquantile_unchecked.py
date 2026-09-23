def _nanquantile_unchecked(
        a,
        q,
        axis=None,
        out=None,
        overwrite_input=False,
        method="linear",
        keepdims=np._NoValue,
):
    """Assumes that q is in [0, 1], and is an ndarray"""
    # apply_along_axis in _nanpercentile doesn't handle empty arrays well,
    # so deal them upfront
    if a.size == 0:
        return np.nanmean(a, axis, out=out, keepdims=keepdims)
    r, k = function_base._ureduce(a,
                                  func=_nanquantile_ureduce_func,
                                  q=q,
                                  axis=axis,
                                  out=out,
                                  overwrite_input=overwrite_input,
                                  method=method)
    if keepdims and keepdims is not np._NoValue:
        return r.reshape(q.shape + k)
    else:
        return r
