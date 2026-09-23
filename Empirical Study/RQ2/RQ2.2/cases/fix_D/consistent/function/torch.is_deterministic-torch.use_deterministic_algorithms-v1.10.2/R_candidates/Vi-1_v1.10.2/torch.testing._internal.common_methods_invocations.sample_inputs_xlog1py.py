def sample_inputs_xlog1py(self, device, dtype, requires_grad):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def generator():
        # same shape
        yield SampleInput(make_arg((S, S)), args=(make_arg((S, S), low=-1),))
        # rhs broadcast
        yield SampleInput(make_arg((S, S)), args=(make_arg((S,), low=-1),))
        # all zero `x`
        with torch.no_grad():
            x = make_arg((S, S))
            x.fill_(0)
        yield SampleInput(x, args=(make_arg((S, S), low=-1),))

        # randomly zero-masked `x`
        x = make_arg((S, S))
        y = make_arg((S, S), low=-1)
        with torch.no_grad():
            x[torch.rand(x.shape) > 0.5] = 0
        yield SampleInput(x, args=(y,))

        # Scalar x
        # `input` has to be a tensor
        # yield SampleInput(0, args=(make_arg((S, S), low=-1),))
        # yield SampleInput(2.1, args=(make_arg((S, S), low=-1),))

        # Scalar y
        yield SampleInput(make_arg((S, S)), args=(-0.5,))
        yield SampleInput(make_arg((S, S)), args=(1.2,))

    return list(generator())
