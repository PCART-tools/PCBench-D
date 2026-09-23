def sample_inputs_masked_reduction(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for masked reduction operators.

    Masked reduction operator is a reduction operator with trailing
    mask optional argument. A mask is a bool tensor with the same
    shape as input or a shape that is broadcastable to input shape.
    """
    inputs: List[SampleInput] = []
    kwargs['supports_multiple_dims'] = op_info.supports_multiple_dims
    for sample_input in sample_inputs_reduction(op_info, device, dtype, requires_grad, **kwargs):
        for mask in _generate_masked_op_mask(sample_input.input.shape, device, **kwargs):
            sample_input_args, sample_input_kwargs = sample_input.args, dict(mask=mask, **sample_input.kwargs)
            inputs.append(SampleInput(sample_input.input.clone().requires_grad_(requires_grad),
                                      args=sample_input_args, kwargs=sample_input_kwargs))
            if(not requires_grad and dtype.is_floating_point and
               sample_input.input.ndim == 2 and mask is not None and
               mask.shape == sample_input.input.shape):
                for v in [torch.inf, -torch.inf, torch.nan]:
                    t = sample_input.input.clone()
                    t.diagonal()[:] = v
                    inputs.append(SampleInput(t.detach().requires_grad_(requires_grad),
                                              args=sample_input_args,
                                              kwargs=sample_input_kwargs))

    return inputs
