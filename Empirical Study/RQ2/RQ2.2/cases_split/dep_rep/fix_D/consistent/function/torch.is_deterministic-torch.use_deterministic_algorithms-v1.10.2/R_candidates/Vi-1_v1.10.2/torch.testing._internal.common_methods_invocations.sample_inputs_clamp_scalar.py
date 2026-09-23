def sample_inputs_clamp_scalar(op_info, device, dtype, requires_grad):
    tensors = (
        make_tensor((2, 3, 2), device, dtype, low=None, high=None, requires_grad=requires_grad),
        make_tensor((2, 0, 3), device, dtype, low=None, high=None, requires_grad=requires_grad),
    )
    if dtype is torch.uint8:
        min_max_vals = ((2, 5), (3, 7))
    else:
        min_max_vals = ((0, 1), (-1, 1))
    output = [SampleInput(tensor, args=vals) for tensor, vals in product(tensors, min_max_vals)]
    output += [SampleInput(tensors[0], args=(0.5, None)), SampleInput(tensors[0], args=(None, 0.5))]
    empty_tensor = make_tensor((), device=device, dtype=dtype, low=None, high=None, requires_grad=requires_grad)
    output += [SampleInput(empty_tensor, args=(0.0, 1.0)), ]
    return output
