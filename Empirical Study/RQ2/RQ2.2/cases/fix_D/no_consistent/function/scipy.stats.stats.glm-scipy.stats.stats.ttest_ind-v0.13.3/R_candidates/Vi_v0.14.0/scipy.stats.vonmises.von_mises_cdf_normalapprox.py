def von_mises_cdf_normalapprox(k,x,C1):
    b = np.sqrt(2/np.pi)*np.exp(k)/i0(k)
    z = b*np.sin(x/2.)
    return scipy.stats.norm.cdf(z)
