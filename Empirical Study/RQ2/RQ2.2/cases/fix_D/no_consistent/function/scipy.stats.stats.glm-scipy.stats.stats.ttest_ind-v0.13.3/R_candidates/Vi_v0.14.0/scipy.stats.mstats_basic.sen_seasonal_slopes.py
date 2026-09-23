def sen_seasonal_slopes(x):
    x = ma.array(x, subok=True, copy=False, ndmin=2)
    (n,_) = x.shape
    # Get list of slopes per season
    szn_slopes = ma.vstack([(x[i+1:]-x[i])/np.arange(1,n-i)[:,None]
                            for i in range(n)])
    szn_medslopes = ma.median(szn_slopes, axis=0)
    medslope = ma.median(szn_slopes, axis=None)
    return szn_medslopes, medslope
