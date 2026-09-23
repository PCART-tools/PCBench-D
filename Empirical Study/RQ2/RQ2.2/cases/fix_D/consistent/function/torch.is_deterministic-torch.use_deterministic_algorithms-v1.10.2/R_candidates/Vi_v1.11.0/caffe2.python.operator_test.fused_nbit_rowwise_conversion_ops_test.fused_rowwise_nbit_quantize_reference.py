def fused_rowwise_nbit_quantize_reference(data, bit):
    minimum = np.min(data, axis=1).astype(np.float16).astype(np.float32)
    maximum = np.max(data, axis=1)
    span = maximum - minimum
    qmax = (1 << bit) - 1
    scale = (span / qmax).astype(np.float16).astype(np.float32)
    bias = np.zeros(data.shape[0])
    quantized_data = np.zeros(data.shape).astype(np.uint8)

    for i in range(data.shape[0]):
        bias[i] = minimum[i]
        inverse_scale = 1.0 if scale[i] == 0.0 else 1 / scale[i]
        if scale[i] == 0.0 or math.isinf(inverse_scale):
            scale[i] = 1.0
            inverse_scale = 1.0
        quantized_data[i] = np.clip(
            np.round((data[i, :] - minimum[i]) * inverse_scale), 0, qmax
        )

    # pack
    assert 8 % bit == 0
    num_elem_per_byte = 8 // bit
    packed_dim = (data.shape[1] + num_elem_per_byte - 1) // num_elem_per_byte
    packed_data = np.zeros([data.shape[0], packed_dim]).astype(np.uint8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if j % num_elem_per_byte == 0:
                packed_data[i, j // num_elem_per_byte] = quantized_data[i, j]
            else:
                packed_data[i, j // num_elem_per_byte] += quantized_data[i, j] << (
                    (j % num_elem_per_byte) * bit
                )

    scale_bytes = half_floats_to_bytes(scale.astype(np.float16))
    bias_bytes = half_floats_to_bytes(bias.astype(np.float16))
    return np.concatenate([packed_data, scale_bytes, bias_bytes], axis=1)
