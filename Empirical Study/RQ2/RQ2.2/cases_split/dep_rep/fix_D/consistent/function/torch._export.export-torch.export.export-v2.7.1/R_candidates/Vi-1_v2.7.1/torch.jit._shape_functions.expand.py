def expand(self: list[int], sizes: list[int]):
    assert len(sizes) >= len(self)
    ndim = len(sizes)
    tensor_dim = len(self)
    if ndim == 0:
        return _copy(sizes)
    out: list[int] = []
    for i in range(ndim):
        offset = ndim - 1 - i
        dim = tensor_dim - 1 - offset
        size = self[dim] if dim >= 0 else 1
        targetSize = sizes[i]
        if targetSize == -1:
            assert dim >= 0
            targetSize = size
        if size != targetSize:
            assert size == 1
            size = targetSize
        out.append(size)
    return out
