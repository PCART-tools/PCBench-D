def sample_inputs_masked_softmax(op_info, device, dtype, requires_grad, with_dtype=False, **kwargs):
    """Sample inputs for masked softmax, log_softmax, and softmin.

    Masked normalization operator is a reduction operator with
    trailing mask optional argument. A mask is a bool tensor with the
    same shape as input or a shape that is broadcastable to input
    shape.
    """
    inputs: List[SampleInput] = []
    for sample_input in sample_inputs_softmax_variant(op_info, device, dtype, requires_grad, with_dtype=with_dtype, **kwargs):
        for mask in _generate_masked_op_mask(sample_input.input.shape, device, **kwargs):
            sample_input_args, sample_input_kwargs = sample_input.args, dict(mask=mask, **sample_input.kwargs)
            inputs.append(SampleInput(sample_input.input.clone().requires_grad_(requires_grad),
                                      args=sample_input_args, kwargs=sample_input_kwargs))
    return inputs
