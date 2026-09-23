def sample_inputs_diff(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    test_cases = (
        ((1,), 0, None, None),
        ((S,), 0, None, None),
        ((S, 1), 0, None, None),
        ((S, 1), 1, None, None),
        ((S, S), 0, None, None),
        ((S, S), 1, None, None),
        ((S, S), 0, (1, S), (2, S)),
        ((S, S), 0, None, (2, S)),
        ((S, S, S), 1, None, None),
        ((S, S, S), 2, None, None),
        ((S, S, S), 1, (S, 1, S), (S, 1, S)),
        ((S, S, S), 2, (S, S, 1), (S, S, 1)),
        ((S, S, S), 2, (S, S, S), (S, S, S)),)

    sample_inputs = []
    for size, dim, size_prepend, size_append in test_cases:
        prepend_size = 0 if (size_prepend is None) else size_prepend[dim]
        append_size = 0 if (size_append is None) else size_append[dim]
        dim_size = size[dim] + prepend_size + append_size
        for n in range(dim_size):
            input_tensor = make_arg(size)
            prepend = make_arg(size_prepend) if size_prepend else None
            append = make_arg(size_append) if size_append else None
            sample_inputs.append(SampleInput(input_tensor, args=(n, dim, prepend, append,)))

    # add some samples with n > dim_size
    sample_inputs.append(SampleInput(make_arg((S, S, S)), args=(S + 1, 1,)))
    sample_inputs.append(SampleInput(make_arg((S, S, S)), args=(S * 3 + 2, 2, make_arg((S, S, S)), make_arg((S, S, S)),)))

    return sample_inputs
