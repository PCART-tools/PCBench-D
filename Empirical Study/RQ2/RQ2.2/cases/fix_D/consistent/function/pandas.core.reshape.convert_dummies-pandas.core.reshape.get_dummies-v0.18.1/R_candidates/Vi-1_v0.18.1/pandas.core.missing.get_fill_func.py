def get_fill_func(method):
    method = clean_fill_method(method)
    return _fill_methods[method]
