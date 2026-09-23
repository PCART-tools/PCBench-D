def doc_wraps(func):
    """ Copy docstring from one function to another """
    def _(func2):
        if func.__doc__ is not None:
            func2.__doc__ = func.__doc__.replace('>>>', '>>').replace('...', '..')
        return func2
    return _
