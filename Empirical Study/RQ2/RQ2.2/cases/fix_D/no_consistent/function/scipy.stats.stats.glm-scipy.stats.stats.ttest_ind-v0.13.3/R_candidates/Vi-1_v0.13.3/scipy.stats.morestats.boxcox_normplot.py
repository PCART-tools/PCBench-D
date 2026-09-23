def boxcox_normplot(x,la,lb,plot=None,N=80):
    svals = r_[la:lb:complex(N)]
    ppcc = svals*0.0
    k = 0
    for sval in svals:
        # JP: this doesn't use sval, creates constant ppcc, and horizontal line
        z = boxcox(x,sval)  # JP: this was missing
        r1,r2 = probplot(z,dist='norm',fit=1)
        ppcc[k] = r2[-1]
        k += 1
    if plot is not None:
        plot.plot(svals, ppcc, 'x')
        plot.title('Box-Cox Normality Plot')
        plot.xlabel('Prob Plot Corr. Coef.')
        plot.ylabel('Transformation parameter')
    return svals, ppcc
