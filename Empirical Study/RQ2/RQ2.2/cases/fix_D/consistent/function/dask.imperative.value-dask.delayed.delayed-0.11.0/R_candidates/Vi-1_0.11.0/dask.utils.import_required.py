def import_required(mod_name, error_msg):
    """Attempt to import a required dependency.

    Raises a RuntimeError if the requested module is not available.
    """
    try:
        return import_module(mod_name)
    except ImportError:
        raise RuntimeError(error_msg)
