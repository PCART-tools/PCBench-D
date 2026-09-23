def doc_wraps(func):
    """ Copy docstring from one function to another """
    def _(func2):
        if func.__doc__ is not None:
            func2.__doc__ = skip_doctest(func.__doc__)
        return func2
    return _
