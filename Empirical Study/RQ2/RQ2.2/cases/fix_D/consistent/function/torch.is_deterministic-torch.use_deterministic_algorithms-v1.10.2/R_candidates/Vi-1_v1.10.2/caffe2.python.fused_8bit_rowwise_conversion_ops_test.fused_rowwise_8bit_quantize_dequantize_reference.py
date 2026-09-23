def fused_rowwise_8bit_quantize_dequantize_reference(data):
    fused_quantized = fused_rowwise_8bit_quantize_reference(data)
    scale = bytes_to_floats(fused_quantized[..., -8:-4].astype(np.uint8).reshape(-1, 4))
    scale = scale.reshape(fused_quantized.shape[:-1] + (scale.shape[-1],))
    bias = bytes_to_floats(fused_quantized[..., -4:].astype(np.uint8).reshape(-1, 4))
    bias = bias.reshape(fused_quantized.shape[:-1] + (bias.shape[-1],))
    quantized_data = fused_quantized[..., :-8]
    return quantized_data * scale + bias
