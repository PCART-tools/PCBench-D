def test_override_dispatch(func=None, *, name=None):
    """Auto-converts the first argument into the backend equivalent,
    causing the dispatching mechanism to trigger for every
    decorated algorithm."""
    if func is None:
        if name is None:
            return test_override_dispatch
        return functools.partial(test_override_dispatch, name=name)
    if isinstance(func, str):
        return functools.partial(test_override_dispatch, name=func)
    # If name not provided, use the name of the function
    if name is None:
        name = func.__name__

    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwds):
        backend = plugins[plugin_name].load()
        if not hasattr(backend, name):
            pytest.xfail(f"'{name}' not implemented by {plugin_name}")
        bound = sig.bind(*args, **kwds)
        bound.apply_defaults()
        graph, *args = args
        # Convert graph into backend graph-like object
        #   Include the weight label, if provided to the algorithm
        weight = None
        if "weight" in bound.arguments:
            weight = bound.arguments["weight"]
        elif "data" in bound.arguments and "default" in bound.arguments:
            # This case exists for several MultiGraph edge algorithms
            if isinstance(bound.arguments["data"], str):
                weight = bound.arguments["data"]
            elif bound.arguments["data"]:
                weight = "weight"
        graph = backend.convert_from_nx(graph, weight=weight, name=name)
        result = getattr(backend, name).__call__(graph, *args, **kwds)
        return backend.convert_to_nx(result, name=name)

    _register_algo(name, wrapper)
    return wrapper
