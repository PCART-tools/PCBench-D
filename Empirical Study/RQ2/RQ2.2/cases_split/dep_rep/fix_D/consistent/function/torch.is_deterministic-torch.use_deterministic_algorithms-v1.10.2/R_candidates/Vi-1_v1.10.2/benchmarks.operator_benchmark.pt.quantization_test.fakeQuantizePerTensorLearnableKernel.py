def fakeQuantizePerTensorLearnableKernel(
    input, scale, zero_point,
    quant_min: int, quant_max: int
):
    return torch._fake_quantize_learnable_per_tensor_affine(input, scale, zero_point, quant_min, quant_max)
