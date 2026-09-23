def sample_inputs_atan2(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    cases = (
        ((S, S, S), (S, S, S), False),
        ((), (), False),
        ((S, S, S), (S,), False),
        ((S,), (S, S, S), True),
        ((S, 1, S), (S, S), True),
    )

    def generator():
        for x_shape, y_shape, broadcasts_input in cases:
            yield SampleInput(make_arg(x_shape), args=(make_arg(y_shape),),
                              broadcasts_input=broadcasts_input)

    return list(generator())
