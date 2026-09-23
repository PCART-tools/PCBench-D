def sample_inputs_diff(op_info, device, dtype, requires_grad, **kwargs):
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
        ((S, S, S), 1, (S, 1, S), (S, 1, S)),)

    sample_inputs = []
    for size, dim, size_prepend, size_append in test_cases:
        args = (make_tensor(size, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad), 1, dim,
                make_tensor(size_prepend, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad) if size_prepend else None,
                make_tensor(size_append, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad) if size_append else None)
        sample_inputs.append(SampleInput(args[0], args=args[1:]))

    return tuple(sample_inputs)
