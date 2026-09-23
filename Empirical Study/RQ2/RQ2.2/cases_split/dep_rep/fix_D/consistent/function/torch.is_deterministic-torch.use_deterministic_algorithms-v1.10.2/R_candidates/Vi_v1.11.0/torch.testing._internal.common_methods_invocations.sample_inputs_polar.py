def sample_inputs_polar(op_info, device, dtype, requires_grad, **kwargs):
    def _make_tensor_helper(shape, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    samples = (
        SampleInput(_make_tensor_helper((S, S), low=0), args=(_make_tensor_helper((S, S)),)),
        SampleInput(_make_tensor_helper((), low=0), args=(_make_tensor_helper(()),)),
    )

    return samples
