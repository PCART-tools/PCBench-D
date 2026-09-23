def sample_inputs_layer_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, normalized_shape and a kwarg dict for eps
    cases: Tuple[Tuple[int], Tuple[int], dict] = (  # type: ignore[assignment]
        ((1, 2, 3), (1, 2, 3), {'eps': 0.5}),
        ((2, 2, 3), (2, 3), {'eps': -0.5}),
        ((1,), (1,), {}),
        ((1, 2), (2,), {}),
        ((0, 1), (1,), {}),
    )

    def generator():
        for input_shape, normalized_shape, kwargs in cases:
            # Shape of weight and bias should be the same as normalized_shape
            weight = make_arg(normalized_shape)
            bias = make_arg(normalized_shape)
            yield SampleInput(
                make_arg(input_shape),
                args=(normalized_shape, weight, bias),
                kwargs=kwargs
            )
        # Without any optional args
        yield SampleInput(make_arg((1, 2)), args=((2,),))

        # TODO: @krshrimali, once to_numpy method in SampleInput class is modified to take None inputs,
        # enable these inputs; see https://github.com/pytorch/pytorch/pull/63276#discussion_r691950400

        # With weight and a `None` bias
        # yield SampleInput(make_arg((1, 2)), args=((2,), make_arg((2,)), None))

        # With `None` weight and bias (tests failing for this, see the link above)
        # yield SampleInput(make_arg((1, 2)), args=((2,), None, make_arg((2,))))

    return list(generator())
