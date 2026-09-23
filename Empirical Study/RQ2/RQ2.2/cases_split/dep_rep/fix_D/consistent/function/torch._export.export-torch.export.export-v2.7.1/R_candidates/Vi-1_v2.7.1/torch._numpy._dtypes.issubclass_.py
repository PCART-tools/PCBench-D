def issubclass_(arg, klass):
    try:
        return issubclass(arg, klass)
    except TypeError:
        return False
