@doc_wraps(scipy.stats.skew)
def skew(a, axis=0, bias=True, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")

    n = a.shape[axis]  # noqa; for bias
    m2 = moment(a, 2, axis)
    m3 = moment(a, 3, axis)
    zero = (m2 == 0)
    vals = da.where(~zero, m3 / m2**1.5, 0.)
    # vals = da.where(~zero, (m2, m3),
    #                 lambda m2, m3: m3 / m2**1.5,
    #                 0.)
    if not bias:
        # Need a version of np.place
        raise NotImplementedError("bias=False is not implemented.")

    if vals.ndim == 0:
        return vals
        # TODO: scalar
        # return vals.item()

    return vals
