@normalizer
@linalg_errors
def solve(a: ArrayLike, b: ArrayLike):
    a, b = _atleast_float_2(a, b)
    return torch.linalg.solve(a, b)
