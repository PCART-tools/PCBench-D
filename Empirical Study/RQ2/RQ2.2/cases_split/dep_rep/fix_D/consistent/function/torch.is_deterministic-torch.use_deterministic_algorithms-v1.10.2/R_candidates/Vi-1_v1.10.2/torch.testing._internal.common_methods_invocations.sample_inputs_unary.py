def sample_inputs_unary(op_info, device, dtype, requires_grad, **kwargs):
    low, high = op_info.domain
    low = low if low is None else low + op_info._domain_eps
    high = high if high is None else high - op_info._domain_eps

    return (SampleInput(make_tensor((L,), device=device, dtype=dtype,
                                    low=low, high=high,
                                    requires_grad=requires_grad)),
            SampleInput(make_tensor((), device=device, dtype=dtype,
                                    low=low, high=high,
                                    requires_grad=requires_grad)))
