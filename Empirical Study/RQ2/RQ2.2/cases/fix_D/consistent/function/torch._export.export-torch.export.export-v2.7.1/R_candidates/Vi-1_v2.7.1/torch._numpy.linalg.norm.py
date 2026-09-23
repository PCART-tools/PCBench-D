@normalizer
@linalg_errors
def norm(x: ArrayLike, ord=None, axis=None, keepdims: KeepDims = False):
    x = _atleast_float_1(x)
    return torch.linalg.norm(x, ord=ord, dim=axis)
