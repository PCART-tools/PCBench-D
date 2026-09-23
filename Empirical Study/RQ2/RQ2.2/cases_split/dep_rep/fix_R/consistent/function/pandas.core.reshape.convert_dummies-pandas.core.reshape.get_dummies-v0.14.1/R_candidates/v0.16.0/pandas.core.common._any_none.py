def _any_none(*args):
    for arg in args:
        if arg is None:
            return True
    return False
