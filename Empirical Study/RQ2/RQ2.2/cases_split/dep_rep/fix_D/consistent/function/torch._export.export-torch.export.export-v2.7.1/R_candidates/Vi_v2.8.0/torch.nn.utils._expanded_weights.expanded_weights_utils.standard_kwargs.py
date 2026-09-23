def standard_kwargs(kwarg_names, expanded_args):
    r"""Separate args and kwargs from `__torch_function__`s that standardize kwargs.

    Most `__torch_function__`s standardize the kwargs that they give, so this will separate
    the args and kwargs they pass. Functions that don't are linear and convND.
    """
    kwarg_values = expanded_args[len(expanded_args) - len(kwarg_names) :]
    expanded_args_without_kwargs = expanded_args[
        : len(expanded_args) - len(kwarg_names)
    ]
    expanded_kwargs = dict(zip(kwarg_names, kwarg_values))
    return expanded_args_without_kwargs, expanded_kwargs
