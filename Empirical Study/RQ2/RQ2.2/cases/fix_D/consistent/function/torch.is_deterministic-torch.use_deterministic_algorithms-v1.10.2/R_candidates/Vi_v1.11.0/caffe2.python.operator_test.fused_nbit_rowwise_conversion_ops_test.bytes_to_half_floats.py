def bytes_to_half_floats(byte_matrix):
    floats = np.empty([np.shape(byte_matrix)[0], 1], dtype=np.float16)
    for i, byte_values in enumerate(byte_matrix):
        (floats[i],) = np.frombuffer(
            memoryview(byte_values).tobytes(), dtype=np.float16
        )
    return floats
