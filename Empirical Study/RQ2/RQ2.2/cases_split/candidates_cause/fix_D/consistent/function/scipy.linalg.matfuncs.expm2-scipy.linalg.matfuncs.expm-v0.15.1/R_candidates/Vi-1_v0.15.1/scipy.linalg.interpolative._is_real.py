def _is_real(A):
    try:
        if A.dtype == np.complex128:
            return False
        elif A.dtype == np.float64:
            return True
        else:
            raise _DTYPE_ERROR
    except AttributeError:
        raise _TYPE_ERROR
