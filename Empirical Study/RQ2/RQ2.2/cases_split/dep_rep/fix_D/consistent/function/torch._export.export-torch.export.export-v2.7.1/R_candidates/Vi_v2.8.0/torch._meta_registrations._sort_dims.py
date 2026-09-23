def _sort_dims(self: Tensor, dim: list[int], exclude_last: bool = False):
    sorted_dims = list(dim)
    self_strides = self.stride()
    sorted_dims[: len(sorted_dims) - int(exclude_last)].sort(
        key=lambda i: self_strides[i]
    )
    return sorted_dims
