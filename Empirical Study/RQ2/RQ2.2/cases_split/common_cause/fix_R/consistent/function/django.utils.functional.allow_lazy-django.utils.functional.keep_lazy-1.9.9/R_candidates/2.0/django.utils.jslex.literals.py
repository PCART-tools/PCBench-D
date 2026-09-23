def literals(choices, prefix="", suffix=""):
    """
    Create a regex from a space-separated list of literal `choices`.

    If provided, `prefix` and `suffix` will be attached to each choice
    individually.
    """
    return "|".join(prefix + re.escape(c) + suffix for c in choices.split())
