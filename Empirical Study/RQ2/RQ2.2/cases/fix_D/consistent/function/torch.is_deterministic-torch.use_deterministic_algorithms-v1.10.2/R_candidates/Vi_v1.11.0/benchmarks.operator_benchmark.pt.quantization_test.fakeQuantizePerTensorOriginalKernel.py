def fakeQuantizePerTensorOriginalKernel(
    input, scale, zero_point,
    quant_min: int, quant_max: int
):
    return torch.fake_quantize_per_tensor_affine(input, 1.0, 0, quant_min, quant_max)
