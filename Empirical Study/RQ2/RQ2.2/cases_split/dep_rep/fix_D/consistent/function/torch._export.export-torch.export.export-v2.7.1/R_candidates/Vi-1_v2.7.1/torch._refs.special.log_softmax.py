def log_softmax(
    a: TensorLikeType,
    dim: int,
    dtype: Optional[torch.dtype] = None,
) -> TensorLikeType:
    return torch.log_softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]
