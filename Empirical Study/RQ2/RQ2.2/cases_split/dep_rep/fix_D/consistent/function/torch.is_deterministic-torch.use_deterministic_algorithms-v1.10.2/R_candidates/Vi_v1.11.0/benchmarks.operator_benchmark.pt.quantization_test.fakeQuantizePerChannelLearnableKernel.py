def fakeQuantizePerChannelLearnableKernel(
    input, scale, zero_point, axis: int,
    quant_min: int, quant_max: int
):
    return torch._fake_quantize_learnable_per_channel_affine(input, scale, zero_point, axis, quant_min, quant_max)
