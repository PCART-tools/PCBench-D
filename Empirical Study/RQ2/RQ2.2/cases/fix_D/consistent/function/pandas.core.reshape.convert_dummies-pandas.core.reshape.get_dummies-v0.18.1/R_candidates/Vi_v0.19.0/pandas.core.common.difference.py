def difference(a, b):
    return type(a)(list(set(a) - set(b)))
