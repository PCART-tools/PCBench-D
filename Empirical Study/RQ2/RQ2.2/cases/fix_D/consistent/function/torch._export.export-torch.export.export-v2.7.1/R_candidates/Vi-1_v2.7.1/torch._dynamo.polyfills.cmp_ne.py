def cmp_ne(a, b):
    # Check if __ne__ is overridden
    if isinstance(type(a).__ne__, types.FunctionType):
        return a.__ne__(b)
    return not cmp_eq(a, b)
