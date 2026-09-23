@register_decomposition(aten.diagonal)
def diagonal(
    self: TensorLikeType,
    offset: int = 0,
    dim1: int = 0,
    dim2: int = 1,
) -> TensorLikeType:
    """
    Reference implementation of torch.diagonal
    """
    num_dims = self.dim()
    dim1 = utils.canonicalize_dim(idx=dim1, rank=num_dims)
    dim2 = utils.canonicalize_dim(idx=dim2, rank=num_dims)

    torch._check(
        dim1 != dim2, lambda: f"diagonal dimensions cannot be identical {dim1}, {dim2}"
    )

    storage_offset = self.storage_offset()

    if offset >= 0:
        diag_size = max(min(self.size()[dim1], self.size()[dim2] - offset), 0)
    else:
        diag_size = max(min(self.size()[dim1] + offset, self.size()[dim2]), 0)

    if diag_size > 0:
        if offset >= 0:
            storage_offset += offset * self.stride()[dim2]
        else:
            storage_offset -= offset * self.stride()[dim1]

    sizes = [s for i, s in enumerate(self.size()) if i not in (dim1, dim2)]
    sizes.append(diag_size)

    strides = [s for i, s in enumerate(self.stride()) if i not in (dim1, dim2)]
    strides.append(self.stride()[dim1] + self.stride()[dim2])

    result = self.as_strided(size=sizes, stride=strides, storage_offset=storage_offset)

    return result
