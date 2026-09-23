def is_list_like(arg):
    return (hasattr(arg, '__iter__') and
            not isinstance(arg, compat.string_and_binary_types))
