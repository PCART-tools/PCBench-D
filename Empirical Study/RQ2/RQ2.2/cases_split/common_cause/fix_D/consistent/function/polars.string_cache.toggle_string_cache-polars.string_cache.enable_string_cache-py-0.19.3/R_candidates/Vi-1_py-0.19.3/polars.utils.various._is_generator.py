def _is_generator(val: object) -> bool:
    return (
        (isinstance(val, (Generator, Iterable)) and not isinstance(val, Sized))
        or isinstance(val, MappingView)
        or (sys.version_info >= (3, 11) and isinstance(val, _reverse_mapping_views))
    )
