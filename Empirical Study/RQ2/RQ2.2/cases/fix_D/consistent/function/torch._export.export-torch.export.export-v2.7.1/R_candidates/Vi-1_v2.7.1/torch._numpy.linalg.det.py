@normalizer
@linalg_errors
def det(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.det(a)
