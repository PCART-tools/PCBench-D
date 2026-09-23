def _choose_param_value(main_param_name: str, params: Dict[str, Any], default_value: Any) -> Dict[str, Any]:
    """Get a single parameter value, accounting for aliases.

    Parameters
    ----------
    main_param_name : str
        Name of the main parameter to get a value for. One of the keys of ``_ConfigAliases``.
    params : dict
        Dictionary of LightGBM parameters.
    default_value : Any
        Default value to use for the parameter, if none is found in ``params``.

    Returns
    -------
    params : dict
        A ``params`` dict with exactly one value for ``main_param_name``, and all aliases ``main_param_name`` removed.
        If both ``main_param_name`` and one or more aliases for it are found, the value of ``main_param_name`` will be preferred.
    """
    # avoid side effects on passed-in parameters
    params = deepcopy(params)

    aliases = _ConfigAliases.get_sorted(main_param_name)
    aliases = [a for a in aliases if a != main_param_name]

    # if main_param_name was provided, keep that value and remove all aliases
    if main_param_name in params.keys():
        for param in aliases:
            params.pop(param, None)
        return params

    # if main param name was not found, search for an alias
    for param in aliases:
        if param in params.keys():
            params[main_param_name] = params[param]
            break

    if main_param_name in params.keys():
        for param in aliases:
            params.pop(param, None)
        return params

    # neither of main_param_name, aliases were found
    params[main_param_name] = default_value

    return params
