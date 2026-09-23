@normalizer
@linalg_errors
def tensorinv(a: ArrayLike, ind=2):
    a = _atleast_float_1(a)
    return torch.linalg.tensorinv(a, ind=ind)
