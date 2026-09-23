def von_mises_cdf(k,x):
    ix = 2*np.pi*np.round(x/(2*np.pi))
    x = x-ix
    k = float(k)

    # These values should give 12 decimal digits
    CK = 50
    a = [28., 0.5, 100., 5.0]

    if k < CK:
        p = int(np.ceil(a[0]+a[1]*k-a[2]/(k+a[3])))

        F = np.clip(von_mises_cdf_series(k,x,p),0,1)
    else:
        F = von_mises_cdf_normalapprox(k, x)

    return F+ix
