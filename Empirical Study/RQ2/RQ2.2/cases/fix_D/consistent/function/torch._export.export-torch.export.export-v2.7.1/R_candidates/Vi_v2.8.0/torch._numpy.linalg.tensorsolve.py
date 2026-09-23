@normalizer
@linalg_errors
def tensorsolve(a: ArrayLike, b: ArrayLike, axes=None):
    a, b = _atleast_float_2(a, b)
    return torch.linalg.tensorsolve(a, b, dims=axes)
