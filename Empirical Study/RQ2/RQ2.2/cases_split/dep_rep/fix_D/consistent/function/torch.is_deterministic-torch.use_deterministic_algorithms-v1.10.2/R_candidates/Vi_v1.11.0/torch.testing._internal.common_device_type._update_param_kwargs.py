def _update_param_kwargs(param_kwargs, name, value):
    """ Adds a kwarg with the specified name and value to the param_kwargs dict. """
    if isinstance(value, list) or isinstance(value, tuple):
        # Make name plural (e.g. devices / dtypes) if the value is composite.
        param_kwargs['{}s'.format(name)] = value
    elif value:
        param_kwargs[name] = value
