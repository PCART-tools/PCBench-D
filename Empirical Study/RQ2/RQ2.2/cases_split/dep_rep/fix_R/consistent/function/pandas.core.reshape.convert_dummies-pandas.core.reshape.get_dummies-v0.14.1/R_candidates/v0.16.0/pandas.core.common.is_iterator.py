def is_iterator(obj):
    # python 3 generators have __next__ instead of next
    return hasattr(obj, 'next') or hasattr(obj, '__next__')
