def argmax(
    self: list[int], dim: Optional[int] = None, keepdim: bool = False
) -> list[int]:
    if dim is None:
        return []
    return _reduce_along_dim(self, dim, keepdim)
