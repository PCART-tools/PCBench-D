def sample_inputs_fliplr_flipud(op_info, device, dtype, requires_grad, **kwargs):
    tensors = (
        make_tensor((S, M, S), device, dtype, low=None, high=None, requires_grad=requires_grad),
        make_tensor((S, 0, M), device, dtype, low=None, high=None, requires_grad=requires_grad)
    )
    return [SampleInput(tensor) for tensor in tensors]
