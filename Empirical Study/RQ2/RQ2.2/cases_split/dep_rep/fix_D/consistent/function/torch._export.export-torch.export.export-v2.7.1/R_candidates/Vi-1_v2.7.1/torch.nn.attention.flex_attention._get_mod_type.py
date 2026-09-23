def _get_mod_type(fn: Callable) -> _ModificationType:
    """Get the type of modification function.
    This function inspects the number of positional arguments of the function to determine
    the type of modification function. If the function has 5 positional arguments, it is
    considered as a score_mod function. If the function has 4 positional arguments, it is
    considered as a mask function.
    """
    num_positional_args = sum(
        1
        for param in inspect.signature(fn).parameters.values()
        if param.default == inspect.Parameter.empty
    )
    assert num_positional_args == 5 or num_positional_args == 4
    if num_positional_args == 5:
        return _ModificationType.SCORE_MOD
    elif num_positional_args == 4:
        return _ModificationType.MASK_MOD
    else:
        return _ModificationType.UNKNOWN
