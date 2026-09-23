def floats(*args, **kwargs):

    width_supported = hypothesis.version.__version_info__ >= (3, 67, 0)
    if 'width' in kwargs and not width_supported:
        kwargs.pop('width')

    if 'width' not in kwargs and width_supported:
        kwargs['width'] = 32
        if kwargs.get('min_value', None) is not None:
            kwargs['min_value'] = to_float32(kwargs['min_value'])
        if kwargs.get('max_value', None) is not None:
            kwargs['max_value'] = to_float32(kwargs['max_value'])

    return st.floats(*args, **kwargs)
