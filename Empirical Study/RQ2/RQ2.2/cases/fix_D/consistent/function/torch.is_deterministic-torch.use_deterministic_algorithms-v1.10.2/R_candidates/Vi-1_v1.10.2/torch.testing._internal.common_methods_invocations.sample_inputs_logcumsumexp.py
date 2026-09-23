def sample_inputs_logcumsumexp(self, device, dtype, requires_grad):
    inputs = (
        ((S, S, S), 0),
        ((S, S, S), 1),
        ((), 0),
    )
    samples = []

    for shape, dim in inputs:
        t = make_tensor(shape, device, dtype,
                        low=None, high=None,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t, args=(dim,)))

    return tuple(samples)
