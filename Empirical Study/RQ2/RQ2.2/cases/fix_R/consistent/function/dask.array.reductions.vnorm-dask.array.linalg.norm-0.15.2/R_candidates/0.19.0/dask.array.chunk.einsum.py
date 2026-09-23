def einsum(*operands, **kwargs):
    subscripts = kwargs.pop('subscripts')
    ncontract_inds = kwargs.pop('ncontract_inds')
    dtype = kwargs.pop('kernel_dtype')
    chunk = np.einsum(subscripts, *operands, dtype=dtype, **kwargs)

    # Avoid concatenate=True in atop by adding 1's
    # for the contracted dimensions
    return chunk.reshape(chunk.shape + (1,) * ncontract_inds)
