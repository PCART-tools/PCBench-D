@wraps(np.allclose)
def allclose(arr1, arr2, rtol=1e-5, atol=1e-8, equal_nan=False):
    return isclose(arr1, arr2, rtol=rtol, atol=atol, equal_nan=equal_nan).all()
