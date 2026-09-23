def sample_inputs_cov(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    for t in _generate_correlation_inputs(device, dtype, requires_grad):
        inputs.append(SampleInput(t))
        num_observations = t.numel() if t.ndimension() < 2 else t.size(1)
        fweights = make_tensor((num_observations,), device, torch.int, low=0, high=10, requires_grad=requires_grad)
        aweights = make_tensor((num_observations,), device, torch.float, low=0, high=1, requires_grad=requires_grad)
        for correction, fw, aw in product(range(num_observations), [None, fweights], [None, aweights]):
            inputs.append(SampleInput(t, kwargs={'correction': correction, 'fweights': fw, 'aweights': aw}))
    return inputs
