def softmax(
    a: TensorLikeType,
    dim: int,
    dtype: Optional[torch.dtype] = None,
) -> TensorLikeType:
    return torch.softmax(a=a, dim=dim, dtype=dtype)  # type: ignore[call-overload]
