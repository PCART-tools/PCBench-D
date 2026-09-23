def is_final(ann) -> bool:
    return ann.__module__ in {'typing', 'typing_extensions'} and \
        (getattr(ann, '__origin__', None) is Final or isinstance(ann, type(Final)))
