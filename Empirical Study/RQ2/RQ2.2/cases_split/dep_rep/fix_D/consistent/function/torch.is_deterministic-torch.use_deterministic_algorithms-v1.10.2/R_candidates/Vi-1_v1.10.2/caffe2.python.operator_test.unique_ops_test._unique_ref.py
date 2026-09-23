def _unique_ref(x, return_inverse):
    ret = np.unique(x, return_inverse=return_inverse)
    if not return_inverse:
        ret = [ret]
    return ret
