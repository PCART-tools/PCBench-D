def fused_rowwise_nbit_quantize_dequantize_reference(data, bit):
    fused_quantized = fused_rowwise_nbit_quantize_reference(data, bit)
    scale = bytes_to_half_floats(fused_quantized[:, -4:-2].astype(np.uint8)).astype(
        np.float32
    )
    bias = bytes_to_half_floats(fused_quantized[:, -2:].astype(np.uint8)).astype(
        np.float32
    )
    quantized_data = fused_quantized[:, :-4]

    # unpack
    packed_dim = fused_quantized.shape[1] - 4
    assert 8 % bit == 0
    num_elem_per_byte = 8 // bit
    assert packed_dim == ((data.shape[1] + num_elem_per_byte - 1) // num_elem_per_byte)
    unpacked_data = np.zeros(data.shape).astype(np.uint8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            unpacked_data[i, j] = (
                quantized_data[i, j // num_elem_per_byte]
                >> ((j % num_elem_per_byte) * bit)
            ) & ((1 << bit) - 1)

    return scale * unpacked_data + bias
