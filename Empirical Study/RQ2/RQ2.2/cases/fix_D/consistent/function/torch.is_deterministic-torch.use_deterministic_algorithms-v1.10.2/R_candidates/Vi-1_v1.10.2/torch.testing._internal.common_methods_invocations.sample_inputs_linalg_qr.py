def sample_inputs_linalg_qr(op_info, device, dtype, requires_grad=False, **kwargs):
    """
    This function generates input for torch.linalg.qr
    The input is generated as the itertools.product of 'batches' and 'ns'.
    """
    batches = [(), (0,), (2, ), (1, 1)]
    ns = [5, 2, 0]
    out = []
    for batch, (m, n) in product(batches, product(ns, ns)):
        a = torch.randn(*batch, m, n, dtype=dtype, device=device, requires_grad=requires_grad)
        out.append(SampleInput(a))
    return out
