def is_union(ann):
    if ann is Union:
        raise_error_container_parameter_missing("Union")

    return isinstance(ann, BuiltinUnionType) or (
        hasattr(ann, "__module__")
        and ann.__module__ == "typing"
        and (get_origin(ann) is Union)
    )
