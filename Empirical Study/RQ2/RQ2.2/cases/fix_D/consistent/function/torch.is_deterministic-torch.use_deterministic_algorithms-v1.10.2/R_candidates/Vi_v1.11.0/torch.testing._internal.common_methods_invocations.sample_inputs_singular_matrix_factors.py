def sample_inputs_singular_matrix_factors(op_info, device, dtype, requires_grad=False, **kwargs):
    """
    This function produces two tensors of shape (*, m, k) and (*, n, k) with k <= min(m, n).
    Their matrix product could be used to generate tensor of shape (*, m, n) of rank k.
    """

    batches = [(), (0, ), (2, ), (1, 1)]
    size = [1, 5, 10]

    for batch, m, n in product(batches, size, size):
        for k in range(min(3, min(m, n))):
            a = make_tensor((*batch, m, k), device, dtype, requires_grad=requires_grad)
            b = make_tensor((*batch, n, k), device, dtype, requires_grad=requires_grad)
            yield SampleInput(a, args=(b,), kwargs=kwargs)
