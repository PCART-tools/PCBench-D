def sample_inputs_fill_(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       low=None, high=None, requires_grad=requires_grad)

    cases = (((S, S, S), (1,)),
             ((), (1,)),
             # For requires_grad=False below,
             # check https://github.com/pytorch/pytorch/issues/59137
             ((S, S, S), (make_arg((), requires_grad=False),)))

    def generator():
        for shape, args in cases:
            yield SampleInput(make_arg(shape), args=args)

    return list(generator())
