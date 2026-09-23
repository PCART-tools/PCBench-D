def createResolutionCallbackForClassMethods(cls):
    """
    This looks at all the methods defined in a class and pulls their closed-over
    variables into a dictionary and uses that to resolve variables.
    """
    # cls is a type here, so `ismethod` is false since the methods on the type
    # aren't bound to anything, so Python treats them as regular functions
    fns = [getattr(cls, name) for name in cls.__dict__ if inspect.isroutine(getattr(cls, name))]
    captures = {}

    for fn in fns:
        captures.update(get_closure(fn))
        captures.update(get_type_hint_captures(fn))

    def lookup_in_class(key):
        if key in captures:
            return captures[key]
        else:
            return getattr(builtins, key, None)

    return lookup_in_class
