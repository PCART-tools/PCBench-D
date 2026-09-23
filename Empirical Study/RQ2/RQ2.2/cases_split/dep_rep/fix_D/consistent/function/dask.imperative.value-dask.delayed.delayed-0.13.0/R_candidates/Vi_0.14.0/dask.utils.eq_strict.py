def eq_strict(a, b):
    """Returns True if both values have the same type and are equal."""
    if type(a) is type(b):
        return a == b
    return False
