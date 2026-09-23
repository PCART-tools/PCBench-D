def is_tuple(ann) -> bool:
    # Check for typing.Tuple missing args (but `tuple` is fine)
    if ann is typing.Tuple:  # noqa: UP006
        raise_error_container_parameter_missing("Tuple")

    # For some reason Python 3.7 violates the Type[A, B].__origin__ == Type rule
    if not hasattr(ann, "__module__"):
        return False

    ann_origin = get_origin(ann)
    return ann.__module__ in ("builtins", "typing") and ann_origin is tuple
