def sample_inputs_grid_sample(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    batch_size = 2
    num_channels = 3
    modes = ("bilinear", "nearest")
    align_cornerss = (False, True)
    padding_modes = ("zeros", "border", "reflection")

    sample_inputs = []
    for dim in (2, 3):

        modes_ = (*modes, "bicubic") if dim == 2 else modes

        for mode, padding_mode, align_corners in itertools.product(modes_, padding_modes, align_cornerss):
            sample_inputs.append(
                SampleInput(
                    _make_tensor((batch_size, num_channels, *[S] * dim)),
                    args=(_make_tensor((batch_size, *[S] * dim, dim)),),
                    kwargs=dict(
                        mode=mode,
                        padding_mode=padding_mode,
                        align_corners=align_corners,
                    )
                )
            )

    return sample_inputs
