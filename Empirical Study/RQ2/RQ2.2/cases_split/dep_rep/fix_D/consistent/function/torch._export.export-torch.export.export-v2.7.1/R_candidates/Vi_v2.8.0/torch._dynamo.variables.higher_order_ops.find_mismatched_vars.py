def find_mismatched_vars(var, types, allow_none=False):
    """
    Recursively finds variables whose type is not an instance of the specified types.
    Args:
        var: The variable to check.
        types: A tuple of allowed types.
        allow_none (bool): Whether to allow None values. Defaults to False.
    Returns:
        A set of variables whose type is not an instance of the specified types.
    """
    mismatched_vars = set()
    if isinstance(var, (TupleVariable, ListVariable)):
        for item in var.items:
            mismatched_vars.update(find_mismatched_vars(item, types, allow_none))
    elif isinstance(var, ConstDictVariable):
        for value in var.items.values():
            mismatched_vars.update(find_mismatched_vars(value, types, allow_none))
    else:

        def _is_none(var):
            return var.is_python_constant() and var.as_python_constant() is None

        if not isinstance(var, types) and not (allow_none and _is_none(var)):
            mismatched_vars.add(var)
    return mismatched_vars
