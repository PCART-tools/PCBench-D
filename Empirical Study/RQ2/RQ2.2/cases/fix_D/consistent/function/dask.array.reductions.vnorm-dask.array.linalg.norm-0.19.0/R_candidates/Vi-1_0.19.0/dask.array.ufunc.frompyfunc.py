@wraps(np.frompyfunc)
def frompyfunc(func, nin, nout):
    if nout > 1:
        raise NotImplementedError("frompyfunc with more than one output")
    return ufunc(da_frompyfunc(func, nin, nout))
