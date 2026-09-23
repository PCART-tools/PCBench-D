def _get_annotations(obj: type) -> dict[str, Any]:
    return getattr(obj, "__annotations__", {})
