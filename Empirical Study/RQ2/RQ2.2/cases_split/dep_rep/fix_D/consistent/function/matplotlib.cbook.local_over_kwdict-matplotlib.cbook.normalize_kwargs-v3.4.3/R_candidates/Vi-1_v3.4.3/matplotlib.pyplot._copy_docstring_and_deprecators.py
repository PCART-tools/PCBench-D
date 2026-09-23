def _copy_docstring_and_deprecators(method, func=None):
    if func is None:
        return functools.partial(_copy_docstring_and_deprecators, method)
    decorators = [docstring.copy(method)]
    # Check whether the definition of *method* includes @_api.rename_parameter
    # or @_api.make_keyword_only decorators; if so, propagate them to the
    # pyplot wrapper as well.
    while getattr(method, "__wrapped__", None) is not None:
        for decorator_maker, code in _code_objs.items():
            if method.__code__ is code:
                kwargs = {
                    k: v.cell_contents
                    for k, v in zip(code.co_freevars, method.__closure__)}
                assert kwargs["func"] is method.__wrapped__
                kwargs.pop("func")
                decorators.append(decorator_maker(**kwargs))
        method = method.__wrapped__
    for decorator in decorators[::-1]:
        func = decorator(func)
    return func
