def sample_inputs_randint_like(self, device, dtype, requires_grad, **kwargs):
    samples = []
    low = 2
    high = 10

    for sample in sample_inputs_like_fns(self, device, dtype, requires_grad, **kwargs):
        # With high
        samples.append(SampleInput(
            sample.input,
            args=(high,) + sample.args,
            kwargs=sample.kwargs))
        # With low and high
        samples.append(SampleInput(
            get_independent_tensor(sample.input),
            args=(low, high,) + sample.args,
            kwargs=sample.kwargs))
    return tuple(samples)
