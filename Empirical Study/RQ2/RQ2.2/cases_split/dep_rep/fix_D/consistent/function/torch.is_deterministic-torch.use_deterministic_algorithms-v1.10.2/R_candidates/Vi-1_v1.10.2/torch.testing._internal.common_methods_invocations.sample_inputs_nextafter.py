def sample_inputs_nextafter(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (
        ((S, S), (S, S), False),
        ((S, S), (S,), False),
        ((S, ), (S, S), True)
    )

    def generator():
        for shape, other_shape, broadcasts_input in cases:
            yield SampleInput(make_arg(shape), args=(make_arg(other_shape),), broadcasts_input=broadcasts_input)

    return list(generator())
