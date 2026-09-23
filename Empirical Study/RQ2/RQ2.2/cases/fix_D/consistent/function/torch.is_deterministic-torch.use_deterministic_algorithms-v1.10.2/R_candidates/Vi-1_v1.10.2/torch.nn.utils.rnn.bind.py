def bind(optional, fn):
    if optional is None:
        return None
    return fn(optional)
