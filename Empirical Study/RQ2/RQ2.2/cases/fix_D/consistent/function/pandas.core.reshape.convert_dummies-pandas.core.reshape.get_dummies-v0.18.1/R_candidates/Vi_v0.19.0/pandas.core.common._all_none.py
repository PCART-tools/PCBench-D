def _all_none(*args):
    for arg in args:
        if arg is not None:
            return False
    return True
