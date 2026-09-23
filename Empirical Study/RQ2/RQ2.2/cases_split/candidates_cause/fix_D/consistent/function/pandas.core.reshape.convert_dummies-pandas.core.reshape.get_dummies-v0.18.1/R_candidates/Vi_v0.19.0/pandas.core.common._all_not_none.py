def _all_not_none(*args):
    for arg in args:
        if arg is None:
            return False
    return True
