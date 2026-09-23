def sample_inputs_complex(op_info, device, dtype, requires_grad, **kwargs):
    def _make_tensor_helper(shape):
        return make_tensor(shape, device, dtype, requires_grad=requires_grad)

    samples = (
        SampleInput(_make_tensor_helper((S, S)), args=(_make_tensor_helper((S, S)),)),
        SampleInput(_make_tensor_helper(()), args=(_make_tensor_helper(()),)),
    )

    return samples
