def sample_inputs_group_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, num groups, and eps
    cases: Tuple[Tuple[int], int, float] = (  # type: ignore[assignment]
        ((1, 6, 3), 2, 0.5),
        ((2, 6, 3), 2, -0.5),
        ((1, 2), 1, None),
        ((0, 2), 1, None),
    )

    for input_shape, num_groups, eps in cases:
        # Shape of weight and bias should be the same as num_channels
        weight = make_arg(input_shape[1])
        bias = make_arg(input_shape[1])
        kwargs = {'weight': weight, 'bias': bias} if eps is None else {'weight': weight, 'bias': bias, 'eps': eps}
        yield SampleInput(
            make_arg(input_shape),
            args=(num_groups,),
            kwargs=kwargs
        )
    # Without any optional args
    yield SampleInput(make_arg((1, 2)), args=(1,))
