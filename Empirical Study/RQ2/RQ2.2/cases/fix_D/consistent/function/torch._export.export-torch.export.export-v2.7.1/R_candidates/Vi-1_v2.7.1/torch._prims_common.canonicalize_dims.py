def canonicalize_dims(rank, indices, wrap_scalar=True):
    if isinstance(indices, Dim):
        return canonicalize_dim(rank, indices, wrap_scalar)

    return tuple(canonicalize_dim(rank, x, wrap_scalar) for x in indices)
