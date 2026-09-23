def _get_sizeof(obj):
    try:
        return sys.getsizeof(obj)
    except TypeError:
        # occurs on pypy
        if hasattr(obj, '__sizeof__'):
            return int(obj.__sizeof__())
        return 64
