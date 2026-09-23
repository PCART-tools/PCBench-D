def _kolmog1(x,n):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
    j = np.arange(np.floor(n*(1-x))+1)
    return 1 - x * np.sum(np.exp(np.log(misc.comb(n,j))
                                       + (n-j) * np.log(1-x-j/float(n))
                                       + (j-1) * np.log(x+j/float(n))))
