def is_callable_type(type_hint) -> bool:  # type: ignore[no-untyped-def]
    """
    Special Case of is_type.
    """
    return type_hint.__name__ == "Callable"
