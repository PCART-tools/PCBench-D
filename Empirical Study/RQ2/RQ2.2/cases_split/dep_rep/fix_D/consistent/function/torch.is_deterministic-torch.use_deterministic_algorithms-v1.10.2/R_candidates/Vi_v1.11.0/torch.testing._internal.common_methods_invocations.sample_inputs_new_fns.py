def sample_inputs_new_fns(self, device, dtype, requires_grad, **kwargs):
    inputs = [
        ((), (), {}),
        ((S, S), (2, 0), {}),
        ((0, S, 0), (3, 2, 2), {}),
        ((S,), (2, 3), {'dtype': dtype, 'device': device}),
        # Hard-code some dtypes/devices. We want to test cases where the
        # (dtype, device) is different from the input's (dtype, device)
        ((S,), (10,), {'dtype': torch.double}),
        ((S,), (1, 1, 12), {'device': 'cpu'}),
        ((S,), (2, 2, 2), {'dtype': torch.double, 'device': 'cpu'}),
    ]
    if torch.cuda.is_available():
        inputs.append(((S,), (7, 2), {'device': 'cuda'}))

    samples = []
    for input_shape, output_shape, kwargs in inputs:
        t = make_tensor(input_shape, device, dtype,
                        low=None, high=None,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t, args=(output_shape,), kwargs=kwargs))

    return tuple(samples)
