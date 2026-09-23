def von_mises_cdf_series(k,x,p):
    x = float(x)
    s = np.sin(x)
    c = np.cos(x)
    sn = np.sin(p*x)
    cn = np.cos(p*x)
    R = 0
    V = 0
    for n in range(p-1,0,-1):
        sn, cn = sn*c - cn*s, cn*c + sn*s
        R = 1./(2*n/k + R)
        V = R*(sn/n+V)

    return 0.5+x/(2*np.pi) + V/np.pi
