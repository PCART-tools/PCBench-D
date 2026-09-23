@normalizer
@linalg_errors
def eigvalsh(a: ArrayLike, UPLO="L"):
    a = _atleast_float_1(a)
    return torch.linalg.eigvalsh(a, UPLO=UPLO)
