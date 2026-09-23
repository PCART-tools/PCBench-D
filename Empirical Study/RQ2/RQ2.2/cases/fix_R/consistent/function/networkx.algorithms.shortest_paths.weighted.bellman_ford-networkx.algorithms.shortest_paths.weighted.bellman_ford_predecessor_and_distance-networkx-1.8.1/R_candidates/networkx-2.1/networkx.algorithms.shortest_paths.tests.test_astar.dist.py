def dist(a, b):
    """Returns the Euclidean distance between points `a` and `b`."""
    return sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(a, b)))
