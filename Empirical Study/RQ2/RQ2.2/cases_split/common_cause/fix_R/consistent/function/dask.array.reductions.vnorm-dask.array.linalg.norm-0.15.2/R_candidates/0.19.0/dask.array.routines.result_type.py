@wraps(np.result_type)
def result_type(*args):
    args = [a if is_scalar_for_elemwise(a) else a.dtype for a in args]
    return np.result_type(*args)
