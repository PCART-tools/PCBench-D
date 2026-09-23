def solve(input: Tensor, A: Tensor, *, out=None) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.solve` is deprecated in favor of `torch.linalg.solve`. "
        "`torch.linalg.solve` has its arguments reversed and does not return the LU factorization.\n\n"
        "To get the LU factorization see `torch.lu`, which can be used with `torch.lu_solve` or `torch.lu_unpack`.\n"
        "X = torch.solve(B, A).solution "
        "should be replaced with:\n"
        "X = torch.linalg.solve(A, B)"
    )
