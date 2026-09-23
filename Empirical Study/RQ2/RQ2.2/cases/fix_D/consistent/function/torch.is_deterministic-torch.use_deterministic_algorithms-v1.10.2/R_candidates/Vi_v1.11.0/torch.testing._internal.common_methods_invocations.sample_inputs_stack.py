def sample_inputs_stack(op_info, device, dtype, requires_grad, **kwargs):
    tensors = [
        make_tensor((S, S), device, dtype, requires_grad=requires_grad),
        make_tensor((S, S), device, dtype, requires_grad=requires_grad),
        make_tensor((S, S), device, dtype, requires_grad=requires_grad),
    ]

    return (SampleInput(tensors, args=(0,)),)
