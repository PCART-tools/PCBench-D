def log_softmax(
    a: TensorLikeType,
    dim: Optional[int] = None,
    _stacklevel: int = 3,  # for compat when using TorchRefsMode(strict=True)
    dtype: Optional[torch.dtype] = None,
) -> TensorLikeType:
    # The error is for compat with regular PyTorch, which has this behavior
    # deprecated.  For PrimTorch, it's fine to drop support for deprecated
    # behavior because it requires explicit opt in.  This error is to inform
    # users how to update their calls.
    torch._check(dim is not None, lambda: "implicit dim not supported, use dim=X")
    return torch.log_softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]
