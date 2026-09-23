def _vec_from_tensor(x, generator, downcast_complex=False):
    # Create a random vector with the same number of elements as x and the same
    # dtype/device. If x is complex and downcast_complex is False, we create a
    # complex tensor with only real component.
    if x.layout == torch.sparse_coo:
        # For sparse, create a random sparse vec with random values in the same
        # indices. Make sure size is set so that it isn't inferred to be smaller.
        x_values = x._values()
        dtype = _to_real_dtype(x.dtype) if downcast_complex else x.dtype
        values = torch.rand(x_values.numel(), generator=generator) \
            .to(dtype=dtype, device=x.device) \
            .reshape(x_values.shape)
        values /= values.norm()
        vec = torch.sparse_coo_tensor(x._indices(), values, x.size())
    else:
        dtype = _to_real_dtype(x.dtype) if downcast_complex else x.dtype
        vec = torch.rand(x.numel(), generator=generator).to(dtype=dtype, device=x.device)
        vec /= vec.norm()
    return vec
