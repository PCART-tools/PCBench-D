def ttest_rel(a, b, axis=0):
    a, b, axis = _chk2_asarray(a, b, axis)
    if len(a) != len(b):
        raise ValueError('unequal length arrays')

    Ttest_relResult = namedtuple('Ttest_relResult', ('statistic', 'pvalue'))
    if a.size == 0 or b.size == 0:
        return Ttest_relResult(np.nan, np.nan)

    n = a.count(axis)
    df = (n-1.0)
    d = (a-b).astype('d')
    denom = ma.sqrt((n*ma.add.reduce(d*d,axis) - ma.add.reduce(d,axis)**2) / df)
    t = ma.add.reduce(d, axis) / denom
    t = ma.filled(t, 1)
    probs = betai(0.5*df,0.5,df/(df+t*t)).reshape(t.shape).squeeze()

    return Ttest_relResult(t, probs)
