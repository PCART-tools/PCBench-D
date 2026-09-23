def is_sequence(x):
    try:
        iter(x)
        len(x)  # it has a length
        return not isinstance(x, compat.string_and_binary_types)
    except (TypeError, AttributeError):
        return False
