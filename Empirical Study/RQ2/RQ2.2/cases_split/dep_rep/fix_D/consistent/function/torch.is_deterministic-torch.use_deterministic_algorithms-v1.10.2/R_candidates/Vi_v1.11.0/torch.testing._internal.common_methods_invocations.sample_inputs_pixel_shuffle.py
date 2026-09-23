def sample_inputs_pixel_shuffle(op_info, device, dtype, requires_grad, **kwargs):
    return [
        SampleInput(
            make_tensor((1, 9, 2, 2), device=device, dtype=dtype, requires_grad=requires_grad),
            kwargs=dict(upscale_factor=upscale_factor),
        )
        for upscale_factor in (1, 3)
    ]
