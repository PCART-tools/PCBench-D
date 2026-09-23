@dispatch(object)  # type: ignore[no-redef]
def isvar(o):
    return not not _glv and hashable(o) and o in _glv
