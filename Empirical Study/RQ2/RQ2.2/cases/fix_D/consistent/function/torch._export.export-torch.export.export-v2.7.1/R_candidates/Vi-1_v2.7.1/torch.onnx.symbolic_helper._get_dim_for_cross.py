def _get_dim_for_cross(x: _C.Value, dim: int | None):
    if dim == -1:
        tensor_rank = _get_tensor_rank(x)
        assert tensor_rank is not None
        return dim + tensor_rank
    # If dim is not given, it defaults to the first dimension found with the size 3
    if dim is None:
        sizes = _get_tensor_sizes(x)
        assert sizes is not None
        for index, size in enumerate(sizes):
            if size is not None and size == 3:
                return index
    return dim
