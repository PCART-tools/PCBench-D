def raise_error_container_parameter_missing(target_type) -> None:
    if target_type == 'Dict':
        raise RuntimeError(
            "Attempted to use Dict without "
            "contained types. Please add contained type, e.g. "
            "Dict[int, int]"
        )
    raise RuntimeError(
        f"Attempted to use {target_type} without a "
        "contained type. Please add a contained type, e.g. "
        f"{target_type}[int]"
    )
