def ismethod(func):
    """Is func a method?
    Note that this has to work as the method is defined but before the class is
    defined.  At this stage methods look like functions.
    """
    if hasattr(inspect, "signature"):
        signature = inspect.signature(func)
        return signature.parameters.get("self", None) is not None
    else:
        spec = inspect.getfullargspec(func)  # type: ignore[union-attr, assignment]
        return spec and spec.args and spec.args[0] == "self"
