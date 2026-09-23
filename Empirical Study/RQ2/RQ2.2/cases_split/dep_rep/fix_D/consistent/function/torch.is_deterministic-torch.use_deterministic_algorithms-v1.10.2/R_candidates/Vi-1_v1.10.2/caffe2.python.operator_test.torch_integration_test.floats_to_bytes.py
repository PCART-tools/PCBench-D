def floats_to_bytes(floats):
    byte_matrix = np.empty([np.shape(floats)[0], 4], dtype=np.uint8)
    for i, value in enumerate(floats):
        assert isinstance(value, np.float32), (value, floats)
        as_bytes = struct.pack("f", value)
        # In Python3 bytes will be a list of int, in Python2 a list of string
        if isinstance(as_bytes[0], int):
            byte_matrix[i] = list(as_bytes)
        else:
            byte_matrix[i] = [ord(i) for i in as_bytes]
    return byte_matrix
