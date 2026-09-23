def sample_inputs_rbinops(op_info, device, dtype, requires_grad, supports_dtype_kwargs=True, **kwargs):
    def _make_tensor_helper(shape, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    scalar: Union[int, float, complex] = 3

    if dtype.is_floating_point:
        scalar = 3.14
    elif dtype.is_complex:
        scalar = 3.14j

    samples = [
        SampleInput(_make_tensor_helper((S, S, S)), args=(scalar,)),
        SampleInput(_make_tensor_helper(()), args=(scalar,)),
    ]

    return samples
