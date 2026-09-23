def reset_parameter(**kwargs: Union[list, Callable]) -> Callable:
    """Create a callback that resets the parameter after the first iteration.

    .. note::

        The initial parameter will still take in-effect on first iteration.

    Parameters
    ----------
    **kwargs : value should be list or callable
        List of parameters for each boosting round
        or a callable that calculates the parameter in terms of
        current number of round (e.g. yields learning rate decay).
        If list lst, parameter = lst[current_round].
        If callable func, parameter = func(current_round).

    Returns
    -------
    callback : callable
        The callback that resets the parameter after the first iteration.
    """
    def _callback(env: CallbackEnv) -> None:
        new_parameters = {}
        for key, value in kwargs.items():
            if isinstance(value, list):
                if len(value) != env.end_iteration - env.begin_iteration:
                    raise ValueError(f"Length of list {key!r} has to equal to 'num_boost_round'.")
                new_param = value[env.iteration - env.begin_iteration]
            else:
                new_param = value(env.iteration - env.begin_iteration)
            if new_param != env.params.get(key, None):
                new_parameters[key] = new_param
        if new_parameters:
            env.model.reset_parameter(new_parameters)
            env.params.update(new_parameters)
    _callback.before_iteration = True  # type: ignore
    _callback.order = 10  # type: ignore
    return _callback
