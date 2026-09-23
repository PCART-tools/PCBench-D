def _prep_ndarray(values, copy=True):
    if not isinstance(values, (np.ndarray, Series, Index)):
        if len(values) == 0:
            return np.empty((0, 0), dtype=object)

        def convert(v):
            return com._possibly_convert_platform(v)

        # we could have a 1-dim or 2-dim list here
        # this is equiv of np.asarray, but does object conversion
        # and platform dtype preservation
        try:
            if com.is_list_like(values[0]) or hasattr(values[0], 'len'):
                values = np.array([convert(v) for v in values])
            else:
                values = convert(values)
        except:
            values = convert(values)

    else:

        # drop subclass info, do not copy data
        values = np.asarray(values)
        if copy:
            values = values.copy()

    if values.ndim == 1:
        values = values.reshape((values.shape[0], 1))
    elif values.ndim != 2:
        raise ValueError('Must pass 2-d input')

    return values
