def get_supported_modules():
    """
    :returns: A list of all supported modules.
    """
    return [f for f in modules if check_module(f)]
