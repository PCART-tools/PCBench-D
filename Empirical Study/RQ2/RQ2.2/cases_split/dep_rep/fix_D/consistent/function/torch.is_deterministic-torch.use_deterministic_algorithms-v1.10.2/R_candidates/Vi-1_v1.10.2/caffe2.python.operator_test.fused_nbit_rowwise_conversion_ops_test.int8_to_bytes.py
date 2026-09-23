def int8_to_bytes(int8s):
    byte_matrix = np.empty([np.shape(int8s)[0], 1], dtype=np.uint8)
    for i, value in enumerate(int8s):
        assert isinstance(value, np.int8), (value, int8s)
        as_bytes = struct.pack("b", value)
        # In Python3 bytes will be a list of int, in Python2 a list of string
        if isinstance(as_bytes[0], int):
            byte_matrix[i] = list(as_bytes)
        else:
            byte_matrix[i] = [ord(i) for i in as_bytes]
    return byte_matrix
