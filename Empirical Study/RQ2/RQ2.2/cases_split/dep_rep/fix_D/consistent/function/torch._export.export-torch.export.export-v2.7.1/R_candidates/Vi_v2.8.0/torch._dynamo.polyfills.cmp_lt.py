def cmp_lt(a, b):
    result = a.__lt__(b)
    if result is NotImplemented:
        raise TypeError(f"{type(a)} does not support the < operator")
    return result
