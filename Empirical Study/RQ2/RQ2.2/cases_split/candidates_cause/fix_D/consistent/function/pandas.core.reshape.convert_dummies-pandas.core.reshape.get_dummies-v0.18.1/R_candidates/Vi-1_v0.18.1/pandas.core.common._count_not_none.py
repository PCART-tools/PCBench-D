def _count_not_none(*args):
    return sum(x is not None for x in args)
