def sample_inputs_allclose(op_info, device, dtype, requires_grad, **kwargs):
    samples = []
    sample_shapes = [(), (S), (S, S, S)]
    atols = [1e-2, 1e-16]
    rtols = [1e-1, 0.5]
    eps = 1e-8
    for s, rtol, atol in product(sample_shapes, rtols, atols):
        # close sample
        t = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        close = (t + atol).detach().requires_grad_(requires_grad)
        close_sample = SampleInput(t, args=(close,), kwargs=dict(rtol=rtol, atol=atol))
        samples.append(close_sample)

        # random sample
        a = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        b = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        r_sample = SampleInput(a, args=(b,), kwargs=dict(rtol=rtol, atol=atol))
        samples.append(r_sample)

    return samples
