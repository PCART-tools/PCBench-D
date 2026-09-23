def bytes_to_floats(byte_matrix):
    floats = np.empty([np.shape(byte_matrix)[0], 1], dtype=np.float32)
    for i, byte_values in enumerate(byte_matrix):
        (floats[i],) = struct.unpack("f", bytearray(byte_values))
    return floats
