def _ptr_to_numpy(ptr: int, len: int, ptr_type: Any) -> np.ndarray[Any, Any]:
    """
    Create a memory block view as a numpy array.

    Parameters
    ----------
    ptr
        C/Rust ptr casted to usize.
    len
        Length of the array values.
    ptr_type
        Example:
            f32: ctypes.c_float)

    Returns
    -------
    numpy.ndarray
        View of memory block as numpy array.

    """
    ptr_ctype = ctypes.cast(ptr, ctypes.POINTER(ptr_type))
    return np.ctypeslib.as_array(ptr_ctype, (len,))
