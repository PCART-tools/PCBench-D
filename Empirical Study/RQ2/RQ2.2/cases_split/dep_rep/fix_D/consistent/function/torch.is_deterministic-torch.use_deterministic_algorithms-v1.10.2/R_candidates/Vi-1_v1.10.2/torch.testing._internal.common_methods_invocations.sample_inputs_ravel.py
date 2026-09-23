def sample_inputs_ravel(op_info, device, dtype, requires_grad, **kwargs):
    samples = (SampleInput(make_tensor((S, S, S), device, dtype,
                                       low=None, high=None,
                                       requires_grad=requires_grad)),
               SampleInput(make_tensor((), device, dtype,
                                       low=None, high=None,
                                       requires_grad=requires_grad)),)

    return samples
