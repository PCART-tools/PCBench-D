def _check_not_tuple_of_2_elements(obj: Any, obj_name: str = 'obj') -> None:
    """Check object is not tuple or does not have 2 elements."""
    if not isinstance(obj, tuple) or len(obj) != 2:
        raise TypeError(f"{obj_name} must be a tuple of 2 elements.")
