@doc_wraps(scipy.stats.kurtosis)
def kurtosis(a, axis=0, fisher=True, bias=True, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")
    n = a.shape[axis]  # noqa; for bias
    m2 = moment(a, 2, axis)
    m4 = moment(a, 4, axis)
    zero = (m2 == 0)
    olderr = np.seterr(all='ignore')
    try:
        vals = da.where(zero, 0, m4 / m2**2.0)
    finally:
        np.seterr(**olderr)

    if not bias:
        # need a version of np.place
        raise NotImplementedError("bias=False is not implemented.")

    if vals.ndim == 0:
        return vals  # TODO: scalar
        # vals = vals.item()  # array scalar

    if fisher:
        return vals - 3
    else:
        return vals
