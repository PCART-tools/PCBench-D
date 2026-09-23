def from_imperative(*args, **kwargs):
    warn("Deprecation warning: moved to from_delayed")
    return from_delayed(*args, **kwargs)
