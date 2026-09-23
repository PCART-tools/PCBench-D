def sample_inputs_view_as_real(op_info, device, dtype, requires_grad, **kwargs):
    tensors = (
        make_tensor((S, S), device, dtype, requires_grad=requires_grad),
        make_tensor((), device, dtype, requires_grad=requires_grad)
    )
    return [SampleInput(tensor) for tensor in tensors]
