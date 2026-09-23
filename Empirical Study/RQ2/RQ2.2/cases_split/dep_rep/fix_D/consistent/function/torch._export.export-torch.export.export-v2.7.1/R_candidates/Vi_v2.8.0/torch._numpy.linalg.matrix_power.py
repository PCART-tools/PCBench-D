@normalizer
@linalg_errors
def matrix_power(a: ArrayLike, n):
    a = _atleast_float_1(a)
    return torch.linalg.matrix_power(a, n)
