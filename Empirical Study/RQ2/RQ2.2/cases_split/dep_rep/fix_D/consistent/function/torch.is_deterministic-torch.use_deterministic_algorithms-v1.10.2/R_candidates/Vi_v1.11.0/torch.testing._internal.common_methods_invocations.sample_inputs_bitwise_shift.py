def sample_inputs_bitwise_shift(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = (
        (S, S, S),
        (S,),
        (),
    )

    sample_inputs = []
    for size in test_cases:
        tensor1 = make_tensor(size, device, dtype, low=-32, high=32, requires_grad=requires_grad)
        tensor2 = make_tensor(size, device, dtype, low=0, high=5, requires_grad=requires_grad)
        sample_inputs.append(SampleInput(tensor1, args=(tensor2,)))
        sample_inputs.append(SampleInput(tensor1, args=(2,)))

    return tuple(sample_inputs)
