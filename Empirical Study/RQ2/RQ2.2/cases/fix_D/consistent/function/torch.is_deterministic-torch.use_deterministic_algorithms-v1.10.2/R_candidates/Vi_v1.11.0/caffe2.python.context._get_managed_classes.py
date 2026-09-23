def _get_managed_classes(obj):
    return [
        cls for cls in inspect.getmro(obj.__class__)
        if issubclass(cls, Managed) and cls != Managed and cls != DefaultManaged
    ]
