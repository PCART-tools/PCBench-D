def logsumexp(x):
    return np.log(np.sum(np.exp(x), axis=0))
