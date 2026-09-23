def sample_inputs_view_as_complex(op_info, device, dtype, requires_grad, **kwargs):
    return [SampleInput(make_tensor((S, 2), device, dtype, requires_grad=requires_grad),)]
