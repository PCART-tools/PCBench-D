def is_dict(ann) -> bool:
    # Check for typing.Dict missing args (but `dict` is fine)
    if ann is typing.Dict:  # noqa: UP006
        raise_error_container_parameter_missing("Dict")

    if not hasattr(ann, "__module__"):
        return False

    ann_origin = get_origin(ann)
    return ann.__module__ in ("builtins", "typing") and ann_origin is dict
