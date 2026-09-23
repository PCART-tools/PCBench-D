def _get_fill_func(method):
    method = _clean_fill_method(method)
    return _fill_methods[method]
