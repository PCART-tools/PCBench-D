def sample_inputs_repeat_interleave(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        SampleInput(make_input(()), kwargs=dict(repeats=2)),
        SampleInput(make_input((2, 3, 4)), kwargs=dict(repeats=2)),
        SampleInput(make_input((2, 3, 4)), kwargs=dict(repeats=2, dim=1)),
        SampleInput(make_input((2, 3, 4)), kwargs=dict(repeats=torch.arange(3, device=device), dim=1))
    ]
