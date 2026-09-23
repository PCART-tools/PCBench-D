def name(x):
    try:
        return str(hash(x))
    except TypeError:
        return str(hash(str(x)))
