def sample_inputs_t(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    return (SampleInput(make_arg((1, 2))),
            SampleInput(make_arg((2,))),
            SampleInput(make_arg(())))
