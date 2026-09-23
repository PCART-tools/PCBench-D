def boxcox_normmax(x,brack=(-1.0,1.0)):
    N = len(x)
    # compute uniform median statistics
    Ui = zeros(N)*1.0
    Ui[-1] = 0.5**(1.0/N)
    Ui[0] = 1-Ui[-1]
    i = arange(2,N)
    Ui[1:-1] = (i-0.3175)/(N+0.365)
    # this function computes the x-axis values of the probability plot
    #  and computes a linear regression (including the correlation)
    #  and returns 1-r so that a minimization function maximizes the
    #  correlation
    xvals = distributions.norm.ppf(Ui)

    def tempfunc(lmbda, xvals, samps):
        y = boxcox(samps,lmbda)
        yvals = sort(y)
        r, prob = stats.pearsonr(xvals, yvals)
        return 1-r
    return optimize.brent(tempfunc, brack=brack, args=(xvals, x))
