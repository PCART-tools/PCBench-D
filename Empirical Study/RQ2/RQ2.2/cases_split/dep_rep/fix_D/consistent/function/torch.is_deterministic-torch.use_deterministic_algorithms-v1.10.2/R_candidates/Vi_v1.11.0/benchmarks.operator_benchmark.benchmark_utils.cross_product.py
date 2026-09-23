def cross_product(*inputs):
    """
    Return a list of cartesian product of input iterables.
    For example, cross_product(A, B) returns ((x,y) for x in A for y in B).
    """
    return (list(itertools.product(*inputs)))
