def _check_module_exists(name):
    import importlib.util
    return importlib.util.find_spec(name) is not None
