def _load_lib():
    """Load LightGBM library."""
    lib_path = find_lib_path()
    if len(lib_path) == 0:
        return None
    lib = ctypes.cdll.LoadLibrary(lib_path[0])
    lib.LGBM_GetLastError.restype = ctypes.c_char_p
    callback = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
    lib.callback = callback(_log_callback)
    if lib.LGBM_RegisterLogCallback(lib.callback) != 0:
        raise LightGBMError(lib.LGBM_GetLastError().decode('utf-8'))
    return lib
