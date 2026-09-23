def _copy_docstring_and_deprecators(method, func=None):
    if func is None:
        return functools.partial(_copy_docstring_and_deprecators, method)
    decorators = [docstring.copy(method)]
    # Check whether the definition of *method* includes @_api.rename_parameter
    # or @_api.make_keyword_only decorators; if so, propagate them to the
    # pyplot wrapper as well.
    while getattr(method, "__wrapped__", None) is not None:
        decorator = _api.deprecation.DECORATORS.get(method)
        if decorator:
            decorators.append(decorator)
        method = method.__wrapped__
    for decorator in decorators[::-1]:
        func = decorator(func)
    return func
