def cint32_array_to_numpy(cptr, length):
    """Convert a ctypes int pointer array to a numpy array."""
    if isinstance(cptr, ctypes.POINTER(ctypes.c_int32)):
        return np.ctypeslib.as_array(cptr, shape=(length,)).copy()
    else:
        raise RuntimeError('Expected int32 pointer')
