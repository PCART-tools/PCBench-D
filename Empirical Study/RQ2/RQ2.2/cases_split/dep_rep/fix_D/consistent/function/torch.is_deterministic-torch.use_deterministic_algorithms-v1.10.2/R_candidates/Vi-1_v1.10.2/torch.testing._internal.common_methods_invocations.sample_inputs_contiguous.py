def sample_inputs_contiguous(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    def generator():
        yield SampleInput(make_arg((S, S)))
        yield SampleInput(make_arg((S, S), noncontiguous=True))

    return list(generator())
