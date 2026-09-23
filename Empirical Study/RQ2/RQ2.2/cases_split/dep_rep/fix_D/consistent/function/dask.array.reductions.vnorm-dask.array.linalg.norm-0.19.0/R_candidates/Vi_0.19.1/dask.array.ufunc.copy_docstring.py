@curry
def copy_docstring(target, source=None):
    target.__doc__ = skip_doctest(source.__doc__)
    return target
