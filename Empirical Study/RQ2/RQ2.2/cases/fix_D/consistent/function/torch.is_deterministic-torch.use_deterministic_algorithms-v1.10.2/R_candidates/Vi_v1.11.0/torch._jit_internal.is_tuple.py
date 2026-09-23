def is_tuple(ann) -> bool:
    if ann is Tuple:
        raise_error_container_parameter_missing("Tuple")

    # For some reason Python 3.7 violates the Type[A, B].__origin__ == Type rule
    if not hasattr(ann, '__module__'):
        return False
    return ann.__module__ == 'typing' and \
        (getattr(ann, '__origin__', None) is Tuple or
            getattr(ann, '__origin__', None) is tuple)
