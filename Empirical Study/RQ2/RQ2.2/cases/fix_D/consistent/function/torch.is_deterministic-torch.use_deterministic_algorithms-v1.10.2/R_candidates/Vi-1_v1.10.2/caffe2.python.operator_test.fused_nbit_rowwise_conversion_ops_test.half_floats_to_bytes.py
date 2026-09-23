def half_floats_to_bytes(floats):
    byte_matrix = np.empty([np.shape(floats)[0], 2], dtype=np.uint8)
    for i, value in enumerate(floats):
        assert isinstance(value, np.float16), (value, floats)
        byte_matrix[i] = np.frombuffer(
            memoryview(np.array([value])).tobytes(), dtype=np.uint8
        )
    return byte_matrix
