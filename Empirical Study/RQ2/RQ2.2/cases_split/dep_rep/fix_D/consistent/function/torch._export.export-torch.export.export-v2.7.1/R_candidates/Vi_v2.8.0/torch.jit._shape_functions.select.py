def select(self: list[int], dim: int, index: int):
    ndim = len(self)
    assert ndim != 0
    dim = maybe_wrap_dim(dim, ndim)
    size = self[dim]
    assert not (index < -size or index >= size)
    if index < 0:
        index += size
    out: list[int] = []
    for i in range(ndim):
        if i != dim:
            out.append(self[i])
    return out
