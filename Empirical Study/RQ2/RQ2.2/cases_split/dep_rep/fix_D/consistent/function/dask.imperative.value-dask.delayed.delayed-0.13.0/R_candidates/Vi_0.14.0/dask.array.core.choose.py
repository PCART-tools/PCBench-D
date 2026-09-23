@wraps(np.choose)
def choose(a, choices):
    return elemwise(variadic_choose, a, *choices)
