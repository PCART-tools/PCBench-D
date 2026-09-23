def sample_inputs_full_like(self, device, dtype, requires_grad, **kwargs):
    def get_val(dtype):
        return make_tensor([], 'cpu', dtype).item()

    inputs = [
        ((), get_val(dtype), {}),
        ((S, S), get_val(dtype), {}),
        ((0, S, 0), get_val(dtype), {}),
        ((S,), get_val(dtype), {'dtype': dtype, 'device': device}),
        # Hard-code some dtypes/devices. We want to test cases where the
        # (dtype, device) is different from the input's (dtype, device)
        ((S,), get_val(torch.double), {'dtype': torch.double}),
        ((S,), get_val(dtype), {'device': 'cpu'}),
        ((S,), get_val(torch.double), {'dtype': torch.double, 'device': 'cpu'}),
    ]
    if torch.cuda.is_available():
        inputs.append(((S,), get_val(dtype), {'device': 'cuda'}))

    samples = []
    for shape, fill_value, kwargs in inputs:
        t = make_tensor(shape, device, dtype,
                        low=None, high=None,
                        requires_grad=requires_grad)
        samples.append(SampleInput(t, args=(fill_value,), kwargs=kwargs))

    return tuple(samples)
