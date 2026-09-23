def sample_inputs_softplus(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, (S,), device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        SampleInput(make_input()),
        SampleInput(make_input(), kwargs=dict(beta=3)),
        SampleInput(make_input(low=1), kwargs=dict(threshold=1)),
    ]
