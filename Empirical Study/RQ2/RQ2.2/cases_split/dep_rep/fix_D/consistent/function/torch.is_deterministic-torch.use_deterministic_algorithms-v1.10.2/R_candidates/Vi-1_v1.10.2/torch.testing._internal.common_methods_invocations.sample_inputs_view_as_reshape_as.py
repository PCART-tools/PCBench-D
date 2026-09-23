def sample_inputs_view_as_reshape_as(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device)

    cases = (((S, S, S), (S * S, S)),
             ((), ()),
             ((), (1, 1)),
             )

    def generator():
        for case in cases:
            shape, shape_other = case
            inp = make_arg(shape, requires_grad=requires_grad)
            yield(SampleInput(inp, args=(make_arg(shape_other, requires_grad=False),)))

            if op_info.name != "view_as" and len(shape) >= 2:
                yield(SampleInput(inp.transpose(0, 1), args=(make_arg(shape_other, requires_grad=False),)))

    return list(generator())
