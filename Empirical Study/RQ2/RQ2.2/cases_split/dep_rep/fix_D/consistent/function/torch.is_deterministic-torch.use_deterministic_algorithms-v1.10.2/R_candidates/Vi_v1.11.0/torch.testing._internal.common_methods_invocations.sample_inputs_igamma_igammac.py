def sample_inputs_igamma_igammac(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, low=1e-3)
    cases = (((S, S), (S, S), False),
             ((S, S), (S, ), False),
             ((S, ), (S, S), True),
             ((), (), False))

    for shape, other_shape, broadcasts_input in cases:
        yield SampleInput(make_arg(shape, requires_grad=requires_grad),
                          args=(make_arg(other_shape, requires_grad=False),),
                          broadcasts_input=broadcasts_input)
