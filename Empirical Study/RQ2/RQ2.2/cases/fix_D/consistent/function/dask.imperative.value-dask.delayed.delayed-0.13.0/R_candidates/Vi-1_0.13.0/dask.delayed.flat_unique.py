def flat_unique(ls):
    """Flatten ``ls``, filter by unique id, and return a list"""
    return list(unique(chain.from_iterable(ls), key=id))
