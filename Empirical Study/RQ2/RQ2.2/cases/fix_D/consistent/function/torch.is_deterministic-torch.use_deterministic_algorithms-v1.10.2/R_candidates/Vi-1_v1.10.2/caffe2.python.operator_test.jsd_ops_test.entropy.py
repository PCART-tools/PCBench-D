def entropy(p):
    q = 1. - p
    return -p * np.log(p) - q * np.log(q)
