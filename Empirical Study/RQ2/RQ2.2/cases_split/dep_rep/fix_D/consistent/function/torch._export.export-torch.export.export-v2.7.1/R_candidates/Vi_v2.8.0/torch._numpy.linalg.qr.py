@normalizer
@linalg_errors
def qr(a: ArrayLike, mode="reduced"):
    a = _atleast_float_1(a)
    result = torch.linalg.qr(a, mode=mode)
    if mode == "r":
        # match NumPy
        result = result.R
    return result
