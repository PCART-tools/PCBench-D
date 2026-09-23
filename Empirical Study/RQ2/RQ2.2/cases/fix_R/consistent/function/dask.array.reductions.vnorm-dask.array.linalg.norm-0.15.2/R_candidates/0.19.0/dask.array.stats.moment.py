@doc_wraps(scipy.stats.moment)
def moment(a, moment=1, axis=0, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")
    return da.moment(a, moment, axis=axis)
