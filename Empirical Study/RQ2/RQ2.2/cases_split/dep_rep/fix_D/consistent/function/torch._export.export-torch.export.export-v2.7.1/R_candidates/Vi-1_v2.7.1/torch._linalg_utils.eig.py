def eig(
    self: Tensor,
    eigenvectors: bool = False,
    *,
    e=None,
    v=None,
) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.linalg.eig` returns complex tensors of dtype `cfloat` or `cdouble` rather than real tensors "
        "mimicking complex tensors.\n\n"
        "L, _ = torch.eig(A) "
        "should be replaced with:\n"
        "L_complex = torch.linalg.eigvals(A)\n\n"
        "and\n\n"
        "L, V = torch.eig(A, eigenvectors=True) "
        "should be replaced with:\n"
        "L_complex, V_complex = torch.linalg.eig(A)"
    )
