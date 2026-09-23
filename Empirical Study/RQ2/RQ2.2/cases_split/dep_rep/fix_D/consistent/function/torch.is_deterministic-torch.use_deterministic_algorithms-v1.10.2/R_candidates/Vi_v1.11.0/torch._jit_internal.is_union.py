def is_union(ann):
    if ann is Union:
        raise_error_container_parameter_missing("Union")

    return (hasattr(ann, '__module__') and
            ann.__module__ == 'typing' and
            (getattr(ann, '__origin__', None) is Union))
