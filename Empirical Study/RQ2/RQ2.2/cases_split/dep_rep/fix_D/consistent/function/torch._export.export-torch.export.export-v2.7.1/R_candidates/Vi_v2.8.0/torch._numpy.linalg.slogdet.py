@normalizer
@linalg_errors
def slogdet(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.slogdet(a)
