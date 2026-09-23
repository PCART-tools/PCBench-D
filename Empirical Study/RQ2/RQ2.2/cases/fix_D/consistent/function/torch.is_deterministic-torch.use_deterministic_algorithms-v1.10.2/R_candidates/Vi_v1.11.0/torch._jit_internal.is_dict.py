def is_dict(ann) -> bool:
    if ann is Dict:
        raise_error_container_parameter_missing("Dict")

    if not hasattr(ann, '__module__'):
        return False
    return ann.__module__ == 'typing' and \
        (getattr(ann, '__origin__', None) is Dict or
            getattr(ann, '__origin__', None) is dict)
