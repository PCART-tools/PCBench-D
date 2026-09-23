def sample_inputs_nn_functional_prelu(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases = (
        (()),
        ((S, )),
        ((S, S)),
        ((S, M, S))
    )

    for shape in cases:
        for weight in [-1., 0., 0.8, 1.]:
            weight_tensor = torch.tensor(weight, device=device, dtype=dtype, requires_grad=requires_grad)
            yield SampleInput(make_arg(shape), kwargs=dict(weight=weight_tensor))

        if len(shape) >= 2:
            channel_size = shape[1]
            yield SampleInput(make_arg(shape), kwargs=dict(weight=make_arg((channel_size,))))
