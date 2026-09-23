@normalizer
@linalg_errors
def svd(a: ArrayLike, full_matrices=True, compute_uv=True, hermitian=False):
    a = _atleast_float_1(a)
    if not compute_uv:
        return torch.linalg.svdvals(a)

    # NB: ignore the hermitian= argument (no pytorch equivalent)
    result = torch.linalg.svd(a, full_matrices=full_matrices)
    return result
