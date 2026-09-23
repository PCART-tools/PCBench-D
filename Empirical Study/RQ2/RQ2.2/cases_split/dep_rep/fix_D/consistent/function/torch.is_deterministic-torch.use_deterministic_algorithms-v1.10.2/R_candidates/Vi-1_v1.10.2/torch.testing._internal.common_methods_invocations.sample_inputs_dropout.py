def sample_inputs_dropout(op_info, device, dtype, requires_grad, **kwargs):
    input = make_tensor((S,), device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        SampleInput(input),
        SampleInput(input, kwargs=dict(p=0.0)),
        SampleInput(input, kwargs=dict(p=1.0)),
        SampleInput(input, kwargs=dict(training=False)),
    ]
