def boxcox_llf(lmb, data):
    """The boxcox log-likelihood function.
    """
    N = len(data)
    y = boxcox(data,lmb)
    my = np.mean(y, axis=0)
    f = (lmb-1)*sum(log(data),axis=0)
    f -= N/2.0*log(sum((y-my)**2.0/N,axis=0))
    return f
