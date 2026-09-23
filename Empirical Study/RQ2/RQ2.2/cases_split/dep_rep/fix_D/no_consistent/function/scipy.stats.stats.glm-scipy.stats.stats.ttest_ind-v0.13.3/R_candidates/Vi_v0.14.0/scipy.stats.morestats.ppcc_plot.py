def ppcc_plot(x,a,b,dist='tukeylambda', plot=None, N=80):
    """Returns (shape, ppcc), and optionally plots shape vs. ppcc
    (probability plot correlation coefficient) as a function of shape
    parameter for a one-parameter family of distributions from shape
    value a to b.

    See also ppcc_max
    """
    svals = r_[a:b:complex(N)]
    ppcc = svals*0.0
    k = 0
    for sval in svals:
        r1,r2 = probplot(x,sval,dist=dist,fit=1)
        ppcc[k] = r2[-1]
        k += 1
    if plot is not None:
        plot.plot(svals, ppcc, 'x')
        plot.title('(%s) PPCC Plot' % dist)
        plot.xlabel('Prob Plot Corr. Coef.')
        plot.ylabel('Shape Values')
    return svals, ppcc
