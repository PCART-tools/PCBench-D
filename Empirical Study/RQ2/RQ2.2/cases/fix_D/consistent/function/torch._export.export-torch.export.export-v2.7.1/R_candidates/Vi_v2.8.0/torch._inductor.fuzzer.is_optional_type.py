def is_optional_type(type_hint) -> bool:  # type: ignore[no-untyped-def]
    """
    Special case of is_type.
    """
    origin = get_origin(type_hint)

    if origin is Union:
        args = get_args(type_hint)
        return type(None) in args

    return False
