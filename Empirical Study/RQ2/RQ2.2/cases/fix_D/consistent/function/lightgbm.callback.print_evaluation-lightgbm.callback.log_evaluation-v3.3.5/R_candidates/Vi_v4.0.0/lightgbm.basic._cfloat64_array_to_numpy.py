def _cfloat64_array_to_numpy(cptr: "ctypes._Pointer", length: int) -> np.ndarray:
    """Convert a ctypes double pointer array to a numpy array."""
    if isinstance(cptr, ctypes.POINTER(ctypes.c_double)):
        return np.ctypeslib.as_array(cptr, shape=(length,)).copy()
    else:
        raise RuntimeError('Expected double pointer')
