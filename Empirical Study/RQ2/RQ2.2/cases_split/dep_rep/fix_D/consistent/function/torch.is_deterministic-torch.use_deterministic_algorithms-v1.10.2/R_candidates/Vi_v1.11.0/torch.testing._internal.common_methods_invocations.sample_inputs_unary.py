def sample_inputs_unary(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs):
    if not op_kwargs:
        op_kwargs = {}

    low, high = op_info.domain
    low = low if low is None else low + op_info._domain_eps
    high = high if high is None else high - op_info._domain_eps

    if op_info.supports_sparse_csr:
        # Tensors with dim=2 for sparse CSR testing
        yield SampleInput(make_tensor((L, L), device=device, dtype=dtype,
                                      low=low, high=high,
                                      requires_grad=requires_grad), kwargs=op_kwargs)
    else:
        # Creates a 1D, empty, and scalar tensor
        for shape in ((L,), (1, 0, 3), ()):
            yield SampleInput(make_tensor(shape, device=device, dtype=dtype,
                                          low=low, high=high,
                                          requires_grad=requires_grad), kwargs=op_kwargs)
