def _dispatch(func=None, *, name=None):
    """Dispatches to a backend algorithm
    when the first argument is a backend graph-like object.
    """
    # Allow any of the following decorator forms:
    #  - @_dispatch
    #  - @_dispatch()
    #  - @_dispatch("override_name")
    #  - @_dispatch(name="override_name")
    if func is None:
        if name is None:
            return _dispatch
        return functools.partial(_dispatch, name=name)
    if isinstance(func, str):
        return functools.partial(_dispatch, name=func)
    # If name not provided, use the name of the function
    if name is None:
        name = func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        graph = args[0]
        if hasattr(graph, "__networkx_plugin__") and plugins:
            plugin_name = graph.__networkx_plugin__
            if plugin_name in plugins:
                backend = plugins[plugin_name].load()
                if hasattr(backend, name):
                    return getattr(backend, name).__call__(*args, **kwds)
                else:
                    raise NetworkXNotImplemented(
                        f"'{name}' not implemented by {plugin_name}"
                    )
        return func(*args, **kwds)

    _register_algo(name, wrapper)
    return wrapper
