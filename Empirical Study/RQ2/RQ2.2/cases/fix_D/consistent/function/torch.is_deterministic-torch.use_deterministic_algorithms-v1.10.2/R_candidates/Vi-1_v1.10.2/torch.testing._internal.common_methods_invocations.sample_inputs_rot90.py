def sample_inputs_rot90(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    args = ((1, (0, 1),),
            (1, (1, 2),),
            (1, (1, -1),),
            ())

    def generator():
        for arg in args:
            yield SampleInput(make_arg((S, S, S)), args=arg)

    return list(generator())
