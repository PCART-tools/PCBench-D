def _ensure_numeric(x):
    if isinstance(x, np.ndarray):
        if is_integer_dtype(x) or is_bool_dtype(x):
            x = x.astype(np.float64)
        elif is_object_dtype(x):
            try:
                x = x.astype(np.complex128)
            except:
                x = x.astype(np.float64)
            else:
                if not np.any(x.imag):
                    x = x.real
    elif not (is_float(x) or is_integer(x) or is_complex(x)):
        try:
            x = float(x)
        except Exception:
            try:
                x = complex(x)
            except Exception:
                raise TypeError('Could not convert %s to numeric' % str(x))
    return x
