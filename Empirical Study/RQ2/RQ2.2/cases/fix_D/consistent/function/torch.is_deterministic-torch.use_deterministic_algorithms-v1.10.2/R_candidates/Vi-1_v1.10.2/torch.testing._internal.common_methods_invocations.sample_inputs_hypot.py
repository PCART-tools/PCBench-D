def sample_inputs_hypot(op_info, device, dtype, requires_grad):
    input = make_tensor((S, S), device, dtype, requires_grad=requires_grad)
    args = make_tensor((S, S), device, dtype, requires_grad=requires_grad)

    return (
        SampleInput(input, args=(args,)),
    )
