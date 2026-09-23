def _to_dtype_if_needed(
    tensor: torch.Tensor, dtype: Optional[torch.dtype]
) -> torch.Tensor:
    if dtype is not None and tensor.dtype != dtype:
        return tensor.to(dtype)
    return tensor
