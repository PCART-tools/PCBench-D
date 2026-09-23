def _noarg_wrapper(f, docstring=None, **kargs):
    def wrapper(self):
        result = _na_map(f, self._data, **kargs)
        return self._wrap_result(result)

    wrapper.__name__ = f.__name__
    if docstring is not None:
        wrapper.__doc__ = docstring
    else:
        raise ValueError('Provide docstring')

    return wrapper
