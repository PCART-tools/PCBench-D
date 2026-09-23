def _register_algo(name, wrapped_func):
    if name in _registered_algorithms:
        raise KeyError(f"Algorithm already exists in dispatch registry: {name}")
    _registered_algorithms[name] = wrapped_func
    wrapped_func.dispatchname = name
