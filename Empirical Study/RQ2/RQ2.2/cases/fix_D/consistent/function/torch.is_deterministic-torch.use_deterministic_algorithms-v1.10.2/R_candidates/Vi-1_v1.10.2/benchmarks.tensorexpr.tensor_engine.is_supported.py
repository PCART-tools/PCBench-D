def is_supported(method):
    if hasattr(method, "is_supported"):
        return method.is_supported
    return True
