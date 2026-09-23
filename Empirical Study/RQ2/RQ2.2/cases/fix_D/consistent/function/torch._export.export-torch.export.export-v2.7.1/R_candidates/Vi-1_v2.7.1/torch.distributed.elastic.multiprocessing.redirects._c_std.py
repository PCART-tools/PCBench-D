def _c_std(stream: str):
    return ctypes.c_void_p.in_dll(libc, stream)
