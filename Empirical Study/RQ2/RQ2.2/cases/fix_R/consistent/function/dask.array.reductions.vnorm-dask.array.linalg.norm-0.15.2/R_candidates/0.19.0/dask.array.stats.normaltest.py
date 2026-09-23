@doc_wraps(scipy.stats.normaltest)
def normaltest(a, axis=0, nan_policy='propagate'):
    if nan_policy != 'propagate':
        raise NotImplementedError("`nan_policy` other than 'propagate' "
                                  "have not been implemented.")

    s, _ = skewtest(a, axis)
    k, _ = kurtosistest(a, axis)
    k2 = s * s + k * k
    return delayed(NormaltestResult, nout=2)(k2, delayed(distributions.chi2.sf)(k2, 2))
