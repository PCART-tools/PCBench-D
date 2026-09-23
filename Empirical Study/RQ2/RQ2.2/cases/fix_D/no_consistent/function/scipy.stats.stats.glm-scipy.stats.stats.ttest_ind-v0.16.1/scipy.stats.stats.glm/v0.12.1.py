def glm(data, para):
    """
    Calculates a linear model fit ...
    anova/ancova/lin-regress/t-test/etc. Taken from:

    Returns
    -------
    statistic, p-value ???

    References
    ----------
    Peterson et al. Statistical limitations in functional neuroimaging
    I. Non-inferential methods and statistical models.  Phil Trans Royal Soc
    Lond B 354: 1239-1260.

    """
    if len(para) != len(data):
        raise ValueError("data and para must be same length in aglm")
    n = len(para)
    p = _support.unique(para)
    x = zeros((n,len(p)))  # design matrix
    for l in range(len(p)):
        x[:,l] = para == p[l]
    # fixme: normal equations are bad. Use linalg.lstsq instead.
    b = dot(dot(linalg.inv(dot(np.transpose(x),x)),  # i.e., b=inv(X'X)X'Y
                    np.transpose(x)),data)
    diffs = (data - dot(x,b))
    s_sq = 1./(n-len(p)) * dot(np.transpose(diffs), diffs)

    if len(p) == 2:  # ttest_ind
        c = array([1,-1])
        df = n-2
        fact = np.sum(1.0/np.sum(x,0),axis=0)  # i.e., 1/n1 + 1/n2 + 1/n3 ...
        t = dot(c,b) / np.sqrt(s_sq*fact)
        probs = betai(0.5*df,0.5,float(df)/(df+t*t))
        return t, probs
    else:
        raise ValueError("only ttest_ind implemented")
