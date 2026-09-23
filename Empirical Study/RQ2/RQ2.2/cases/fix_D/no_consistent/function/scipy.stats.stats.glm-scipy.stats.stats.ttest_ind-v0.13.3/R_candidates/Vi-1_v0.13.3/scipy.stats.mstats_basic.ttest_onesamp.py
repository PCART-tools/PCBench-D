def ttest_onesamp(a, popmean):
    a = ma.asarray(a)
    x = a.mean(axis=None)
    v = a.var(axis=None,ddof=1)
    n = a.count(axis=None)
    df = n-1
    svar = ((n-1)*v) / float(df)
    t = (x-popmean)/ma.sqrt(svar*(1.0/n))
    prob = betai(0.5*df,0.5,df/(df+t*t))
    return t,prob
