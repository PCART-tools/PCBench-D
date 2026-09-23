def sample_inputs_unique(op_info, device, dtype, requires_grad, **kwargs):
    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    sample_inputs = []
    for shape, sorted, return_inverse, return_counts, dim in \
            product(sizes, [False, True], [False, True], [False, True], [None, -2, -1, 0, 1, 2]):
        # torch.unique cannot be called if the input tensor has a zero dimension which isn't the selected dim
        if 0 in shape and shape.index(0) is not dim:
            continue

        # skip invalid dim args
        if dim is not None and (dim < -len(shape) or dim >= len(shape)):
            continue

        kwargs = dict(sorted=sorted, return_inverse=return_inverse, return_counts=return_counts, dim=dim)

        # construct a test case with only one distinct value
        input_t = torch.zeros(shape, dtype=dtype, device=device, requires_grad=requires_grad)
        sample_inputs.append(SampleInput(input_t, kwargs=kwargs.copy()))

        # construct a test case with mixed 0s and 1s
        input_t = make_tensor(shape, dtype=torch.bool, device=device, requires_grad=False)\
            .to(dtype).requires_grad_(requires_grad)
        sample_inputs.append(SampleInput(input_t, kwargs=kwargs.copy()))

        # construct a test case with many different values
        input_t = make_tensor(shape, dtype=dtype, device=device, requires_grad=requires_grad)
        sample_inputs.append(SampleInput(input_t, kwargs=kwargs.copy()))

    return sample_inputs
