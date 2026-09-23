def sample_inputs_geqrf(op_info, device, dtype, requires_grad=False):
    batches = [(), (0, ), (2, ), (1, 1)]
    ns = [5, 2, 0]
    samples = []
    for batch, (m, n) in product(batches, product(ns, ns)):
        # TODO: CUDA path doesn't work with batched or empty inputs
        if torch.device(device).type == 'cuda' and (batch != () or m == 0 or n == 0):
            continue
        a = make_tensor((*batch, m, n), device, dtype, low=None, high=None, requires_grad=requires_grad)
        samples.append(SampleInput(a))
    return samples
