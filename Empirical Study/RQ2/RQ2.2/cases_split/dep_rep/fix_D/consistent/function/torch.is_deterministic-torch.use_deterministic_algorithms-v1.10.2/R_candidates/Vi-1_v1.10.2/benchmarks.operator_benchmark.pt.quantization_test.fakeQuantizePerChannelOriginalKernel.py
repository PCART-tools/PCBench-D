def fakeQuantizePerChannelOriginalKernel(
    input, scale, zero_point, axis: int,
    quant_min: int, quant_max: int
):
    return torch.fake_quantize_per_channel_affine(input, scale, zero_point, axis, quant_min, quant_max)
