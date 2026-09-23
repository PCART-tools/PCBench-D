def sample_inputs_bincount(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sample_inputs = []

    for size, weighted in product((S, M), [False, True]):
        input_tensor = torch.randint(0, size, (size,), dtype=dtype, device=device)
        weight_tensor = make_arg((size,)) if weighted else None

        max_val = int(input_tensor.max().item())

        for minlength in [0, max_val // 2, max_val, 2 * max_val]:
            sample_inputs.append(SampleInput(input_tensor,
                                             kwargs=dict(weights=weight_tensor, minlength=minlength)))

    return sample_inputs
