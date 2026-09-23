def sample_inputs_logsumexp(self, device, dtype, requires_grad, **kwargs):
    inputs = (
        ((), (0,), True),
        ((S, S), (1,), True),
        ((S, S), (1,), False)
    )
    samples = []

    for shape, dim, keepdim in inputs:
        t = make_tensor(shape, device, dtype,
                        low=None, high=None,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t, args=(dim, keepdim)))

    return tuple(samples)
