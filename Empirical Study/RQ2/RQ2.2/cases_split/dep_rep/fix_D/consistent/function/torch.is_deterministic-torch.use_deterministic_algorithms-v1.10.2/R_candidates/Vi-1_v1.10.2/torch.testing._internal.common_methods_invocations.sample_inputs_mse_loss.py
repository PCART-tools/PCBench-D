def sample_inputs_mse_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes_and_kwargs = [
        ((), None),
        ((S,), dict(reduction="mean")),
        ((S,), dict(reduction="sum")),
        ((S,), dict(reduction="none")),
        ((S, S), None),
        ((S, S, S), None),
    ]

    return [
        SampleInput(_make_tensor(shape), args=(_make_tensor(shape),), kwargs=kwargs)
        for shape, kwargs in shapes_and_kwargs
    ]
