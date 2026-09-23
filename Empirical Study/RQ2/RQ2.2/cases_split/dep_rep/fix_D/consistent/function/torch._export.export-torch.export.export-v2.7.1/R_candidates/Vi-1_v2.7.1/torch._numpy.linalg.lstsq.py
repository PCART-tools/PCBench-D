@normalizer
@linalg_errors
def lstsq(a: ArrayLike, b: ArrayLike, rcond=None):
    a, b = _atleast_float_2(a, b)
    # NumPy is using gelsd: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/umath_linalg.cpp#L3991
    # on CUDA, only `gels` is available though, so use it instead
    driver = "gels" if a.is_cuda or b.is_cuda else "gelsd"
    return torch.linalg.lstsq(a, b, rcond=rcond, driver=driver)
