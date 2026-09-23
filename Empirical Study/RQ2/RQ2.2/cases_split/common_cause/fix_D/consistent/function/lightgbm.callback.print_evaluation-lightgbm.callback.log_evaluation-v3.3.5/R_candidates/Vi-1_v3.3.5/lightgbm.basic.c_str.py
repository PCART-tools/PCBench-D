def c_str(string):
    """Convert a Python string to C string."""
    return ctypes.c_char_p(string.encode('utf-8'))
