def fused_rowwise_8bit_quantize_reference(data):
    minimum = np.min(data, axis=-1, keepdims=True)
    maximum = np.max(data, axis=-1, keepdims=True)
    span = maximum - minimum
    bias = minimum
    scale = span / 255.0
    inverse_scale = 255.0 / (span + 1e-8)
    quantized_data = round_to_nearest((data - bias) * inverse_scale)
    scale_bytes = floats_to_bytes(scale.reshape(-1))
    scale_bytes = scale_bytes.reshape(data.shape[:-1] + (scale_bytes.shape[-1],))
    bias_bytes = floats_to_bytes(bias.reshape(-1))
    bias_bytes = bias_bytes.reshape(data.shape[:-1] + (bias_bytes.shape[-1],))
    print(quantized_data.shape, scale.shape, scale_bytes.shape, bias.shape, bias_bytes.shape)
    return np.concatenate([quantized_data, scale_bytes, bias_bytes], axis=-1)
