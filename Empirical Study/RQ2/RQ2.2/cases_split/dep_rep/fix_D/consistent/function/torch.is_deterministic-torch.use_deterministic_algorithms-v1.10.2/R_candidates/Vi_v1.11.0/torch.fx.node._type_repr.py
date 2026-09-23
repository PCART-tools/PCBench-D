def _type_repr(obj):
    """Return the repr() of an object, special-casing types (internal helper).
    If obj is a type, we return a shorter version than the default
    type.__repr__, based on the module and qualified name, which is
    typically enough to uniquely identify a type.  For everything
    else, we fall back on repr(obj).
    """
    # HACK: In Python 3.6, type aliases from ``typing`` are instances of ``type``, but in
    # later Python versions, type aliases are not instances of ``type``!! We want
    # all type aliases to fall through to ``repr``, so if we have a type that is
    # in the module typing, don't go down this path.
    if isinstance(obj, type) and obj.__module__ != 'typing':
        if obj.__module__ == 'builtins':
            return obj.__qualname__
        return f'{obj.__module__}.{obj.__qualname__}'
    if obj is ...:
        return('...')
    if isinstance(obj, types.FunctionType):
        return obj.__name__
    return repr(obj)
