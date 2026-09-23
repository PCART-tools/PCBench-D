def bytes_to_scalar(byte_list: List[int], dtype: torch.dtype, device: torch.device):
    dtype_to_ctype: Dict[torch.dtype, Any] = {
        torch.int8: ctypes.c_int8,
        torch.uint8: ctypes.c_uint8,
        torch.int16: ctypes.c_int16,
        torch.int32: ctypes.c_int32,
        torch.int64: ctypes.c_int64,
        torch.bool: ctypes.c_bool,
        torch.float32: ctypes.c_float,
        torch.complex64: ctypes.c_float,
        torch.float64: ctypes.c_double,
        torch.complex128: ctypes.c_double,
    }
    ctype = dtype_to_ctype[dtype]
    num_bytes = ctypes.sizeof(ctype)

    def check_bytes(byte_list):
        for byte in byte_list:
            assert 0 <= byte <= 255

    if dtype.is_complex:
        assert len(byte_list) == (num_bytes * 2)
        check_bytes(byte_list)
        real = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list[:num_bytes])).value
        imag = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list[num_bytes:])).value
        res = real + 1j * imag
    else:
        assert len(byte_list) == num_bytes
        check_bytes(byte_list)
        res = ctype.from_buffer((ctypes.c_byte * num_bytes)(
            *byte_list)).value

    return torch.tensor(res, device=device, dtype=dtype)
