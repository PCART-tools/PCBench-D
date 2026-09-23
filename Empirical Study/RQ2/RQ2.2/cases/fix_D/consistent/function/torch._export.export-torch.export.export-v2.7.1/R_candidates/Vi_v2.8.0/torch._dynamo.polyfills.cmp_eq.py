def cmp_eq(a, b):
    # Note that the commented `is` check should ideally be removed. This is a
    # CPython optimization that skips the __eq__ checks it the obj id's are
    # same. But, these lines adds many `is` nodes in the Fx graph for
    # SymNodeVariable. For now, we can just skip this check. This is STILL
    # correct because one of the __eq__ checks will pass later, just could be
    # slow in some corner cases.
    # if a is b:
    #     return True
    result = a.__eq__(b)
    if result is NotImplemented:
        result = b.__eq__(a)
    return result is not NotImplemented and result
