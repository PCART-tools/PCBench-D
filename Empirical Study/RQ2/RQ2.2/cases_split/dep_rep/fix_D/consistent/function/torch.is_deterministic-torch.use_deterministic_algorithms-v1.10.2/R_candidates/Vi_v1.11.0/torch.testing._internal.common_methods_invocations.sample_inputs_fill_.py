def sample_inputs_fill_(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       low=None, high=None, requires_grad=requires_grad)

    cases = (((S, S, S), (1,)),
             ((), (1,)),
             ((S, S, S), (make_arg(()),)))

    for shape, args in cases:
        yield SampleInput(make_arg(shape), args=args)
