def _format_argument_list(allowed_args: list[str]) -> str:
    """
    Format allowed arguments list for use in the warning message of
    ``deprecate_nonkeyword_arguments``.
    """  # noqa: D205
    if "self" in allowed_args:
        allowed_args.remove("self")
    if not allowed_args:
        return ""
    elif len(allowed_args) == 1:
        return f" except for {allowed_args[0]!r}"
    else:
        last = allowed_args[-1]
        args = ", ".join([f"{x!r}" for x in allowed_args[:-1]])
        return f" except for {args} and {last!r}"
