def sample_inputs_masked_fill(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def sample_generator():
        yield SampleInput(make_arg((S, S)), args=(torch.randn(S, S, device=device) > 0, 10))
        yield SampleInput(make_arg((S, S)), args=(torch.randn(S, S, device=device) > 0, make_arg(())))
        yield SampleInput(make_arg((S, S)), args=(torch.randn(S, device=device) > 0, 10))
        yield SampleInput(make_arg(()), args=(torch.randn((), device=device) > 0, 10))
        yield SampleInput(make_arg(()), args=(torch.randn((), device=device) > 0, make_arg(())))
        yield SampleInput(make_arg((S, S)), args=(torch.randn((), device=device) > 0, 10))

        yield SampleInput(make_arg((S,)),
                          args=(torch.randn(S, S, device=device) > 0, make_arg(())),
                          broadcasts_input=True)
        yield SampleInput(make_arg((S,)),
                          args=(torch.randn(S, S, device=device) > 0, 10),
                          broadcasts_input=True)

    samples = tuple(sample_generator())
    return samples
