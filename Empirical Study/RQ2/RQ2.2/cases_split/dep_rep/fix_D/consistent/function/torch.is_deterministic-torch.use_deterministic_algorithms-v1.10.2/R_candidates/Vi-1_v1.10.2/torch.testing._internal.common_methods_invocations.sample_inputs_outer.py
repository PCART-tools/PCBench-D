def sample_inputs_outer(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    arg_a = make_tensor((S,), device, dtype, requires_grad=requires_grad)
    arg_b = make_tensor((M,), device, dtype, requires_grad=requires_grad)
    inputs.append(SampleInput(arg_a, args=(arg_b,)))
    return inputs
