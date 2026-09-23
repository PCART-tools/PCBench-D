def sample_inputs_std_var(op_info, device, dtype, requires_grad, **kwargs):
    tensor_nd = partial(make_tensor, (S, S, S), device=device, dtype=dtype,
                        requires_grad=requires_grad)
    tensor_1d = partial(make_tensor, (S,), device=device, dtype=dtype,
                        requires_grad=requires_grad)

    return [
        SampleInput(tensor_nd()),
        SampleInput(tensor_nd(), kwargs=dict(dim=1)),
        SampleInput(tensor_nd(), kwargs=dict(dim=1, unbiased=True, keepdim=True)),
        SampleInput(tensor_1d(), kwargs=dict(dim=0, unbiased=True, keepdim=True)),
        SampleInput(tensor_1d(), kwargs=dict(dim=0, unbiased=False, keepdim=False)),

        SampleInput(tensor_nd(), kwargs=dict(dim=(1,), correction=S // 2)),
        SampleInput(tensor_nd(), kwargs=dict(dim=None, correction=0, keepdim=True)),
    ]
