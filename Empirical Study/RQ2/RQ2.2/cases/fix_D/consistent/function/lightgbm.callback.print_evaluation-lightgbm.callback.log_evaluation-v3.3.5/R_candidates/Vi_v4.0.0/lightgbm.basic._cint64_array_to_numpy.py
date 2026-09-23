def _cint64_array_to_numpy(cptr: "ctypes._Pointer", length: int) -> np.ndarray:
    """Convert a ctypes int pointer array to a numpy array."""
    if isinstance(cptr, ctypes.POINTER(ctypes.c_int64)):
        return np.ctypeslib.as_array(cptr, shape=(length,)).copy()
    else:
        raise RuntimeError('Expected int64 pointer')
