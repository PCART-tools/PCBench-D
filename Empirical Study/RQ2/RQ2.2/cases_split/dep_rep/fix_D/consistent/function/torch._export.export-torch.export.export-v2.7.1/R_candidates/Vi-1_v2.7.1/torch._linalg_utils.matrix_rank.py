def matrix_rank(input, tol=None, symmetric=False, *, out=None) -> Tensor:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed.\n"
        "Please use the `torch.linalg.matrix_rank` function instead. "
        "The parameter 'symmetric' was renamed in `torch.linalg.matrix_rank()` to 'hermitian'."
    )
