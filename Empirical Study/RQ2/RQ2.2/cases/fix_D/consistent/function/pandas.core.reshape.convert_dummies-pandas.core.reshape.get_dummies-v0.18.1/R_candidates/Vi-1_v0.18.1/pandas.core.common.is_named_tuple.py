def is_named_tuple(arg):
    return isinstance(arg, tuple) and hasattr(arg, '_fields')
