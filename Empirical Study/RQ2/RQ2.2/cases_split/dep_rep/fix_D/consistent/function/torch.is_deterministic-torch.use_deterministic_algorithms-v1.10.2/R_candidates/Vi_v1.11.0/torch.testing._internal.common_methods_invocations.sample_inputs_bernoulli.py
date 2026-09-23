def sample_inputs_bernoulli(self, device, dtype, requires_grad, **kwargs):
    shapes = [
        [3],
        [],
        [0, 3],
        [2, 3, 4],
    ]

    samples = []
    for shape in shapes:
        t = make_tensor(shape, device, dtype,
                        low=0, high=1,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t))
    return tuple(samples)
