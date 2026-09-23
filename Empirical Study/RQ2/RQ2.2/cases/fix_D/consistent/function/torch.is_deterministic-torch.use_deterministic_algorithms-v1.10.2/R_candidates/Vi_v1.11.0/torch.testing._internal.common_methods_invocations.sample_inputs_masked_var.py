def sample_inputs_masked_var(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for masked var.
    """
    inputs: List[SampleInput] = []
    for unbiased in [False, True]:
        for sample_input in sample_inputs_masked_reduction(op_info, device, dtype, requires_grad, **kwargs):
            if sample_input.args:
                dim = sample_input.args[0]
                sample_input_args = sample_input.args[:1] + (unbiased,) + sample_input.args[1:]
                sample_input_kwargs = sample_input.kwargs.copy()
            else:
                dim = sample_input.kwargs.get('dim')
                sample_input_args = sample_input.args
                sample_input_kwargs = dict(sample_input.kwargs, unbiased=unbiased)
            if requires_grad:
                inmask = torch._masked._input_mask(sample_input.input, *sample_input_args, **sample_input_kwargs)
                orig_count = torch._masked.sum(inmask.new_ones(sample_input.input.shape, dtype=torch.int64),
                                               dim, keepdim=True, mask=inmask)
                if orig_count.min() <= int(unbiased):
                    # Skip samples that lead to singularities in var
                    # computation resulting nan values both in var and
                    # autograd output that test_grad_fn cannot handle
                    # correctly.
                    continue
            inputs.append(SampleInput(sample_input.input.clone().requires_grad_(requires_grad),
                                      args=sample_input_args, kwargs=sample_input_kwargs))
    return inputs
