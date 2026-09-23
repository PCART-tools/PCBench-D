def _rename_keyword_argument(
    old_name: str,
    new_name: str,
    kwargs: dict[str, object],
    func_name: str,
    version: str,
) -> None:
    """Rename a keyword argument of a function."""
    if old_name in kwargs:
        if new_name in kwargs:
            raise TypeError(
                f"`{func_name!r}` received both `{old_name!r}` and `{new_name!r}` as arguments."
                f" `{old_name!r}` is deprecated, use `{new_name!r}` instead"
            )
        issue_deprecation_warning(
            f"`the argument {old_name}` for `{func_name}` is deprecated."
            f" It has been renamed to `{new_name}`.",
            version=version,
        )
        kwargs[new_name] = kwargs.pop(old_name)
