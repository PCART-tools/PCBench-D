def check_arguments(fun, y0, support_complex):
    """Helper function for checking arguments common to all solvers."""
    y0 = np.asarray(y0)
    if np.issubdtype(y0.dtype, np.complexfloating):
        if not support_complex:
            raise ValueError("`y0` is complex, but the chosen solver does "
                             "not support integration in a complex domain.")
        dtype = complex
    else:
        dtype = float
    y0 = y0.astype(dtype, copy=False)

    if y0.ndim != 1:
        raise ValueError("`y0` must be 1-dimensional.")

    if not np.isfinite(y0).all():
        raise ValueError("All components of the initial state `y0` must be finite.")

    def fun_wrapped(t, y):
        return np.asarray(fun(t, y), dtype=dtype)

    return fun_wrapped, y0
