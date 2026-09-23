def check_sample_mean(sm,v,n, popmean):
    # from stats.stats.ttest_1samp(a, popmean):
    # Calculates the t-obtained for the independent samples T-test on ONE group
    # of scores a, given a population mean.
    #
    # Returns: t-value, two-tailed prob
    df = n-1
    svar = ((n-1)*v) / float(df)    # looks redundant
    t = (sm-popmean) / np.sqrt(svar*(1.0/n))
    prob = stats.betai(0.5*df, 0.5, df/(df+t*t))

    # return t,prob
    npt.assert_(prob > 0.01, 'mean fail, t,prob = %f, %f, m, sm=%f,%f' %
            (t, prob, popmean, sm))
