def is_list(ann) -> bool:
    if ann is List:
        raise_error_container_parameter_missing("List")

    if not hasattr(ann, '__module__'):
        return False
    return ann.__module__ == 'typing' and \
        (getattr(ann, '__origin__', None) is List or
            getattr(ann, '__origin__', None) is list)
