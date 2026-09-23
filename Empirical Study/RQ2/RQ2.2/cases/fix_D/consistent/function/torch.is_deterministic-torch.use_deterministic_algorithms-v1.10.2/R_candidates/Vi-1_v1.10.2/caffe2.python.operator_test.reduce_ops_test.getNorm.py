def getNorm(p):
    if p == 1:
        def norm(X, axis, keepdims):
            return np.sum(np.abs(X), axis=axis, keepdims=keepdims)
    elif p == 2:
        def norm(X, axis, keepdims):
            return np.sqrt(np.sum(np.power(X, 2), axis=axis, keepdims=keepdims))
    else:
        raise RuntimeError("Only L1 and L2 norms supported")
    return norm
