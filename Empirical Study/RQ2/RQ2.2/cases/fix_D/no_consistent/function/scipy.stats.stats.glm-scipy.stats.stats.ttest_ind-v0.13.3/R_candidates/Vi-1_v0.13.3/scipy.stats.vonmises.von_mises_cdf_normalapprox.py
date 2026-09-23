def von_mises_cdf_normalapprox(k,x,C1):
    b = np.sqrt(2/np.pi)*np.exp(k)/i0(k)
    z = b*np.sin(x/2.)
    C = 24*k
    chi = z - z**3/((C-2*z**2-16)/3.-(z**4+7/4.*z**2+167./2)/(C+C1-z**2+3))**2
    return scipy.stats.norm.cdf(z)
