def sample_inputs_multinomial(self, device, dtype, requires_grad, **kwargs):
    cases = [
        ([3], 3, dict()),
        ([10], 3, dict()),
        ([3, 10], 3, dict()),
        ([3], 3, dict(replacement=False)),
        ([3], 3, dict(replacement=True)),
        ([3, 4], 4, dict(replacement=True)),
        ([3, 4], 4, dict(replacement=False)),
    ]

    samples = []
    for shape, num_samples, kwargs in cases:
        t = make_tensor(shape, device, dtype,
                        low=0, high=None,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t, args=(num_samples,), kwargs=kwargs))
    return tuple(samples)
