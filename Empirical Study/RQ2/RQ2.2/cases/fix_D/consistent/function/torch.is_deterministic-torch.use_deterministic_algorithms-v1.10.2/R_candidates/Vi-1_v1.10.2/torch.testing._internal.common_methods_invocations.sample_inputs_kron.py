def sample_inputs_kron(op_info, device, dtype, requires_grad):
    test_cases = (
        ((S, S), (M, L)),
    )

    sample_inputs = []
    for input_shape, other_shape in test_cases:
        input = make_tensor(input_shape, device, dtype, low=None, high=None, requires_grad=requires_grad)
        other = make_tensor(other_shape, device, dtype, low=None, high=None, requires_grad=requires_grad)
        sample = SampleInput(input, args=(other,))
        sample_inputs.append(sample)
    return tuple(sample_inputs)
