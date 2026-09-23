def sample_inputs_view_reshape(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((S, S, S), (S * S, S)),
             ((S * S, S), (S, S, S)),
             ((S * S, S), (S, -1, S)),
             ((S * S * 2, S), (S, -1)),
             ((S,), (S,)),
             ((), ()),
             ((), (1,)))

    def generator():
        for case in cases:
            shape, args = case
            inp = make_arg(shape, requires_grad=requires_grad)
            yield(SampleInput(inp, args=(args, )))

            if op_info.name != "view" and len(shape) >= 2:
                yield(SampleInput(inp.transpose(0, 1), args=(args, )))

    return list(generator())
