def fused_rowwise_8bit_quantize_dequantize_reference(data):
    fused_quantized = fused_rowwise_8bit_quantize_reference(data)
    scale = bytes_to_floats(fused_quantized[:, -8:-4].astype(np.uint8))
    bias = bytes_to_floats(fused_quantized[:, -4:].astype(np.uint8))
    quantized_data = fused_quantized[:, :-8]
    return quantized_data * scale + bias
