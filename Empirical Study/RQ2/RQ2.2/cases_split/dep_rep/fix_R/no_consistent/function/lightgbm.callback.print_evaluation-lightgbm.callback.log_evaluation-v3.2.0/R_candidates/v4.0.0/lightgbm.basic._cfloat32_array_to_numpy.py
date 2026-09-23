def _cfloat32_array_to_numpy(cptr: "ctypes._Pointer", length: int) -> np.ndarray:
    """Convert a ctypes float pointer array to a numpy array."""
    if isinstance(cptr, ctypes.POINTER(ctypes.c_float)):
        return np.ctypeslib.as_array(cptr, shape=(length,)).copy()
    else:
        raise RuntimeError('Expected float pointer')
