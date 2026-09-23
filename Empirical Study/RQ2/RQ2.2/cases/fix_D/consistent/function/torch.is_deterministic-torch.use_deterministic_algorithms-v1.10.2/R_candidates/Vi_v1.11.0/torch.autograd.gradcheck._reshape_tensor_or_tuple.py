def _reshape_tensor_or_tuple(u, shape):
    # We don't need to reshape when input corresponding to u is sparse
    if isinstance(u, tuple):
        if u[0].layout != torch.sparse_coo:
            return (u[0].reshape(shape), u[1].reshape(shape))
    else:
        if u.layout != torch.sparse_coo:
            return u.reshape(shape)
    return u
