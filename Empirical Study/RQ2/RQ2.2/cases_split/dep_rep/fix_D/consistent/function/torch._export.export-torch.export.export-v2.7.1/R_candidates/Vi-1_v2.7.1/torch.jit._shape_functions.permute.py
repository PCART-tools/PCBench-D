def permute(input: list[int], dims: list[int]):
    assert len(input) == len(dims)
    ndim = len(dims)
    seen_dims: list[int] = []
    newSizes: list[int] = []
    for i in range(ndim):
        dim = maybe_wrap_dim(dims[i], ndim)
        seen_dims.append(dim)
        newSizes.append(input[dim])
    for i in range(1, ndim):
        for j in range(i):
            assert seen_dims[i] != seen_dims[j]
    return newSizes
