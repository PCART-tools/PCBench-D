def check_module(feature):
    """
    Checks if a module is available.

    :param feature: The module to check for.
    :returns: ``True`` if available, ``False`` otherwise.
    :raises ValueError: If the module is not defined in this version of Pillow.
    """
    if not (feature in modules):
        raise ValueError(f"Unknown module {feature}")

    module, ver = modules[feature]

    try:
        __import__(module)
        return True
    except ImportError:
        return False
