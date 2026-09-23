def deprecate_renamed_function(
    new_name: str, *, version: str
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to mark a function as deprecated due to being renamed."""
    return deprecate_function(f"It has been renamed to `{new_name}`.", version=version)
