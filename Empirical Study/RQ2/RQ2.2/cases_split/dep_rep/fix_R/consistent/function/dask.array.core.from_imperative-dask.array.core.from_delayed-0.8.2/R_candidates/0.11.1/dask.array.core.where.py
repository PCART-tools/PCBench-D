@wraps(np.where)
def where(condition, x=None, y=None):
    if x is None or y is None:
        raise TypeError(where_error_message)
    return choose(condition, [y, x])
