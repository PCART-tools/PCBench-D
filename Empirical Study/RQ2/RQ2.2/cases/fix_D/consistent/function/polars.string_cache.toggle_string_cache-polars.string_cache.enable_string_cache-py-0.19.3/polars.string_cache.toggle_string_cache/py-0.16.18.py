def toggle_string_cache(toggle: bool) -> None:
    """
    Turn on/off the global string cache.

    This ensures that casts to Categorical types have the categories when string values
    are equal.

    """
    _toggle_string_cache(toggle)
