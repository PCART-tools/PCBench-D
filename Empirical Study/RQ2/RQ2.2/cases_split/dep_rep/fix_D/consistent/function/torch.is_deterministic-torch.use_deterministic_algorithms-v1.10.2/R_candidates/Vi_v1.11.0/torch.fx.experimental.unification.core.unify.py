@dispatch(object, object)  # type: ignore[no-redef]
def unify(u, v):
    return unify(u, v, {})
