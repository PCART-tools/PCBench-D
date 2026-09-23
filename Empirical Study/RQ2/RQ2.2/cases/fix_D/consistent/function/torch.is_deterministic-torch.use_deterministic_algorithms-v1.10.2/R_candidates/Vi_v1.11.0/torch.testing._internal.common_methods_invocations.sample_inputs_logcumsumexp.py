def sample_inputs_logcumsumexp(self, device, dtype, requires_grad, **kwargs):
    inputs = (
        ((S, S, S), 0),
        ((S, S, S), 1),
        ((), 0),
    )
    samples = []

    for large_number in (True, False):
        for shape, dim in inputs:
            t = make_tensor(shape, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad)

            if large_number and t.dim() > 0:
                t[0] = 10000
            samples.append(SampleInput(t, args=(dim,)))

    return tuple(samples)
