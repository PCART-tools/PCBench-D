def sample_inputs_max_min_reduction_no_dim(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    inputs.append(SampleInput(make_tensor((S, S, S), device, dtype,
                                          low=None, high=None,
                                          requires_grad=requires_grad),))
    inputs.append(SampleInput(make_tensor((), device, dtype,
                                          low=None, high=None,
                                          requires_grad=requires_grad),))
    return inputs
