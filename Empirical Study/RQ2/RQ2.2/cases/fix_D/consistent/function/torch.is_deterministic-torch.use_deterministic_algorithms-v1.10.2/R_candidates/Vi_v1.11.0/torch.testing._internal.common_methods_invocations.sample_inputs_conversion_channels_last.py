def sample_inputs_conversion_channels_last(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    return [
        # Channels last case: input must be 4d
        SampleInput(make_arg((2, 3, 2, 3)), kwargs={'memory_format': torch.channels_last})

    ]
