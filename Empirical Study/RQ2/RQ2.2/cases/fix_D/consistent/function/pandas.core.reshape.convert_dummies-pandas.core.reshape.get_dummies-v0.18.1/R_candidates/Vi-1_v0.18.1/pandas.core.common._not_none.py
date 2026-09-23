def _not_none(*args):
    return (arg for arg in args if arg is not None)
