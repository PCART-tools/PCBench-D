def normaltest(a, axis=0):
    a, axis = _chk_asarray(a, axis)
    s, _ = skewtest(a, axis)
    k, _ = kurtosistest(a, axis)
    k2 = s*s + k*k

    NormaltestResult = namedtuple('NormaltestResult', ('statistic', 'pvalue'))
    return NormaltestResult(k2, stats.chisqprob(k2, 2))
