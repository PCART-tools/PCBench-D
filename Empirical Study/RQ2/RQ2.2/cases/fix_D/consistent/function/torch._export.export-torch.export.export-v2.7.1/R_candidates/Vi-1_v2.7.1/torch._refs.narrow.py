def narrow(
    a: TensorLikeType, dim: int, start: Union[int, TensorLikeType], length: int
) -> TensorLikeType:
    # Supports Tensor overload that was added for XLA:
    # https://github.com/pytorch/pytorch/issues/31558
    if isinstance(start, TensorLike):
        torch._check(
            start.dim() == 0 and utils.is_integer_dtype(start.dtype),
            lambda: "start must be an 0-dim integral Tensor.",
        )
        start = start.item()  # type: ignore[assignment]
    start = cast(int, start)
    torch._check(a.dim() > 0, lambda: "narrow() cannot be applied to a 0-dim tensor.")
    torch._check(length >= 0, lambda: "narrow(): length must be non-negative.")
    dim = utils.canonicalize_dim(a.ndim, dim)
    dim_length = a.size(dim)
    torch._check_with(
        IndexError,
        -dim_length <= start and start <= dim_length,
        lambda: f"start out of range (expected to be in range of [{-dim_length}, {dim_length}], but got {start})",
    )
    if start < 0:
        start = start + dim_length
    torch._check(
        start <= dim_length - length,
        lambda: f"start ({start}) + length ({length}) exceeds dimension size ({dim_length}).",
    )
    new_shape = list(a.shape)
    new_shape[dim] = length
    return a.as_strided(
        new_shape, a.stride(), a.storage_offset() + a.stride(dim) * start
    )
