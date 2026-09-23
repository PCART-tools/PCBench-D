@normalizer
@linalg_errors
def cond(x: ArrayLike, p=None):
    x = _atleast_float_1(x)

    # check if empty
    # cf: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/linalg.py#L1744
    if x.numel() == 0 and math.prod(x.shape[-2:]) == 0:
        raise LinAlgError("cond is not defined on empty arrays")

    result = torch.linalg.cond(x, p=p)

    # Convert nans to infs (numpy does it in a data-dependent way, depending on
    # whether the input array has nans or not)
    # XXX: NumPy does this: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/linalg.py#L1744
    return torch.where(torch.isnan(result), float("inf"), result)
