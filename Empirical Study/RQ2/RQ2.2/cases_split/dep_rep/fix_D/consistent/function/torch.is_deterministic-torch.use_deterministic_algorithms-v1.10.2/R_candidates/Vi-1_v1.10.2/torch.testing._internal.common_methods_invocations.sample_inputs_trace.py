def sample_inputs_trace(self, device, dtype, requires_grad, **kwargs):
    return (SampleInput((make_tensor((S, S), device, dtype,
                                     low=None, high=None,
                                     requires_grad=requires_grad))),)
