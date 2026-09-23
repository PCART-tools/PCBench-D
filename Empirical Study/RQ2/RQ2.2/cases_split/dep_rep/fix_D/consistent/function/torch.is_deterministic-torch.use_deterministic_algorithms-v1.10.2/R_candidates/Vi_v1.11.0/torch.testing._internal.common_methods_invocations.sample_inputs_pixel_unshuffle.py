def sample_inputs_pixel_unshuffle(op_info, device, dtype, requires_grad, **kwargs):
    return [
        SampleInput(
            make_tensor((1, 1, 6, 6), device=device, dtype=dtype, requires_grad=requires_grad),
            kwargs=dict(downscale_factor=downscale_factor),
        )
        for downscale_factor in (1, 3)
    ]
