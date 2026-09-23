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

    # find a value, and remove other aliases with .pop()
    # prefer the value of 'main_param_name' if it exists, otherwise search the aliases
    found_value = None
    if main_param_name in params.keys():
        found_value = params[main_param_name]

    for param in _ConfigAliases.get(main_param_name):
        val = params.pop(param, None)
        if found_value is None and val is not None:
            found_value = val

    if found_value is not None:
        params[main_param_name] = found_value
    else:
        params[main_param_name] = default_value

    return params
