@dispatch(object, dict)  # type: ignore[no-redef]
def _reify(o, s):
    return o  # catch all, just return the object
