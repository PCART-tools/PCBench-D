def sample_inputs_logit(op_info, device, dtype, requires_grad, **kwargs):
    low, high = op_info.domain

    # Note: Operator is very sensitive at points near the
    # start and end of domain and leads to NaN for float16
    # if domain_eps is 1e-5.
    domain_eps = op_info._domain_eps if dtype != torch.float16 else 3e-2

    low = low + domain_eps
    high = high - domain_eps

    samples = (
        SampleInput(make_tensor((S, S, S), device, dtype, low=low, high=high, requires_grad=requires_grad)),
        SampleInput(make_tensor((S, S, S), device, dtype, low=low,
                                high=high, requires_grad=requires_grad), args=(0.2,)),
        SampleInput(make_tensor((), device, dtype, low=low, high=high, requires_grad=requires_grad)),
        SampleInput(make_tensor((), device, dtype, low=low,
                                high=high, requires_grad=requires_grad), args=(0.2,)),
    )

    return samples
