def _default_alldims(dim: Optional[DimsType], x: TensorLikeType) -> list[int]:
    """Convert Optional[DimsType] to a simple list, defaulting to all dimensions"""
    if dim is None:
        return list(range(x.ndim))
    elif not isinstance(dim, Sequence):
        return [dim]
    else:
        return list(dim)
