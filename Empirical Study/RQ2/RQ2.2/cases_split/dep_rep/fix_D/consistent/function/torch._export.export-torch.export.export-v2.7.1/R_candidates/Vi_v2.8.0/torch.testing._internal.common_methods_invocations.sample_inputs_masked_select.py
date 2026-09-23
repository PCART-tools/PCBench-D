def sample_inputs_masked_select(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)

    yield SampleInput(make_arg((M, M)), torch.randn(M, M, device=device) > 0)

    yield SampleInput(make_arg((M, M)), torch.randn((M,), device=device) > 0)
    yield SampleInput(make_arg((M,)), torch.randn((M, M), device=device) > 0)

    yield SampleInput(make_arg((M, 1, M)), torch.randn((M, M), device=device) > 0)

    yield SampleInput(make_arg(()), torch.tensor(1, device=device, dtype=torch.bool))

    yield SampleInput(make_arg((M, M)), torch.tensor(1, device=device, dtype=torch.bool))

    yield SampleInput(make_arg(()), torch.randn((M, M), device=device) > 0)
