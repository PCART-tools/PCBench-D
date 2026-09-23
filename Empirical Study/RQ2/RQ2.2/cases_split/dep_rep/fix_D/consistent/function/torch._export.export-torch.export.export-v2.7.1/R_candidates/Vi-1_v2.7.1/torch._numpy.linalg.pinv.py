@normalizer
@linalg_errors
def pinv(a: ArrayLike, rcond=1e-15, hermitian=False):
    a = _atleast_float_1(a)
    return torch.linalg.pinv(a, rtol=rcond, hermitian=hermitian)
