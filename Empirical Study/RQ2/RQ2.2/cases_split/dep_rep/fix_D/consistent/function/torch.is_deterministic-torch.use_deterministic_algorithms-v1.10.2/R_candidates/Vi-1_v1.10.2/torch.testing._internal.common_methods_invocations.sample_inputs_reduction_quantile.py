def sample_inputs_reduction_quantile(op_info, device, dtype, requires_grad):
    test_quantiles = (0.5, make_tensor((2,), device, dtype, low=0, high=1))
    test_interpolations = ['linear', 'midpoint']

    inputs = []
    for quantiles in test_quantiles:
        for t in _generate_reduction_inputs(device, dtype, requires_grad):
            # Add case without dim and keepdim kwargs
            inputs.append(SampleInput(t, args=(quantiles,)))
            for kwargs in _generate_reduction_kwargs(t.ndim, supports_multiple_dims=False):
                # Interpolation kwarg for now is only supported when providing both dim and keepdim
                kwargs.setdefault('dim', 0)
                kwargs.setdefault('keepdim', False)
                for interpolation in test_interpolations:
                    kwargs['interpolation'] = interpolation
                    inputs.append(SampleInput(t, args=(quantiles,), kwargs=kwargs))

    return inputs
