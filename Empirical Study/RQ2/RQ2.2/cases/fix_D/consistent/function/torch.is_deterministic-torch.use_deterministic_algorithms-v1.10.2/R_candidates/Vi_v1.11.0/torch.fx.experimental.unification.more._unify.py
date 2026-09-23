@dispatch(slice, slice, dict)
def _unify(u, v, s):
    """ Unify a Python ``slice`` object """
    return unify((u.start, u.stop, u.step), (v.start, v.stop, v.step), s)
