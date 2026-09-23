@normalizer
@linalg_errors
def cholesky(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.cholesky(a)
