def sample_inputs_cumulative_ops(op_info, device, dtype, requires_grad, supports_dtype_kwargs=True, **kwargs):
    def _make_tensor_helper(shape, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    samples = [
        SampleInput(_make_tensor_helper((S, S, S)), args=(0,)),
        SampleInput(_make_tensor_helper((S, S, S)), args=(1,)),
        SampleInput(_make_tensor_helper(()), args=(0,)),
    ]

    if supports_dtype_kwargs:
        # NOTE: if `dtype` is not same as input, then inplace variants fail with
        # `provided dtype must match the dtype of self tensor in cumsum`
        samples.append(SampleInput(_make_tensor_helper((S, S, S)), args=(1,), kwargs={'dtype': dtype}))

    return samples
