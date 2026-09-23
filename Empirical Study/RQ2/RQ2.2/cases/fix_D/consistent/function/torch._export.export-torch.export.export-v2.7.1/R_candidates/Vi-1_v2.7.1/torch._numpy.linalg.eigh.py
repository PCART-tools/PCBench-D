@normalizer
@linalg_errors
def eigh(a: ArrayLike, UPLO="L"):
    a = _atleast_float_1(a)
    return torch.linalg.eigh(a, UPLO=UPLO)
