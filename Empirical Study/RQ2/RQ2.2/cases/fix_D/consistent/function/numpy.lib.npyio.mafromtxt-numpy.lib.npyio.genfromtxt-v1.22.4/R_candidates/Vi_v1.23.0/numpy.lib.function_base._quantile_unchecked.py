def _quantile_unchecked(a,
                        q,
                        axis=None,
                        out=None,
                        overwrite_input=False,
                        method="linear",
                        keepdims=False):
    """Assumes that q is in [0, 1], and is an ndarray"""
    r, k = _ureduce(a,
                    func=_quantile_ureduce_func,
                    q=q,
                    axis=axis,
                    out=out,
                    overwrite_input=overwrite_input,
                    method=method)
    if keepdims:
        return r.reshape(q.shape + k)
    else:
        return r
