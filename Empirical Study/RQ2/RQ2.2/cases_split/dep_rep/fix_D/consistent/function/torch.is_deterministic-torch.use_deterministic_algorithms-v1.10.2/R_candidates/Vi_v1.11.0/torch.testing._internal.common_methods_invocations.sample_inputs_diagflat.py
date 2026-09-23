def sample_inputs_diagflat(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        SampleInput(make_input(())),
        SampleInput(make_input((2,))),
        SampleInput(make_input((2, 2))),
        SampleInput(make_input((2,)), kwargs=dict(offset=1)),
        SampleInput(make_input((2,)), kwargs=dict(offset=-1)),
    ]
