def sample_inputs_cartesian_prod(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(torch.tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # constructs 1-D tensors with varying number of elements
    a = make_arg((0,))
    b = make_arg((0, 1))
    c = make_arg((0, 1, 2, 3))

    samples = []

    # sample with only 1 tensor
    samples.append(SampleInput(
        a
    ))

    # sample with 2 tensors
    samples.append(SampleInput(
        a,
        args=(b,)
    ))

    # sample with 3 tensors
    samples.append(SampleInput(
        a,
        args=(b, c)
    ))

    return tuple(samples)
