def sample_inputs_entr(op_info, device, dtype, requires_grad, **kwargs):
    low, _ = op_info.domain

    if requires_grad:
        low = 0 + op_info._domain_eps

    return (SampleInput(make_tensor((L,), device, dtype,
                                    low=low,
                                    requires_grad=requires_grad)),
            SampleInput(make_tensor((), device, dtype,
                                    low=low,
                                    requires_grad=requires_grad)))
