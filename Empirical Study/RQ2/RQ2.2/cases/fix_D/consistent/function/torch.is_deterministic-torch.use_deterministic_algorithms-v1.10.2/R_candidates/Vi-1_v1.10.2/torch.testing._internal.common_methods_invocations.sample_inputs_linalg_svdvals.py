def sample_inputs_linalg_svdvals(op_info, device, dtype, requires_grad=False, **kwargs):
    batches = [(), (0, ), (2, ), (1, 1)]
    ns = [5, 2, 0]
    samples = []
    for batch, (m, n) in product(batches, product(ns, ns)):
        a = make_tensor((*batch, m, n), device, dtype, low=None, high=None, requires_grad=requires_grad)
        samples.append(SampleInput(a))
    return samples
