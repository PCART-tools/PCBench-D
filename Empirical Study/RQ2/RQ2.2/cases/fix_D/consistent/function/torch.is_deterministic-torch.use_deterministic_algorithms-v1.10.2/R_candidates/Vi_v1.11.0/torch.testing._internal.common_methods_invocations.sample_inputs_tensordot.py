def sample_inputs_tensordot(self, device, dtype, requires_grad, **kwargs):
    cases = (
        ((2, 2, 2), (2, 2, 2), (2)),
        ((2, 2, 1), (2, 1, 2), ([0, 1], [2, 0])),
    )
    samples = []
    for first_shape, second_shape, dims in cases:
        samples.append(SampleInput(make_tensor(first_shape, device, dtype,
                                   requires_grad=requires_grad),
                       args=(make_tensor(second_shape, device, dtype,
                             requires_grad=requires_grad),),
                       kwargs=dict(dims=dims,)))
    return tuple(samples)
