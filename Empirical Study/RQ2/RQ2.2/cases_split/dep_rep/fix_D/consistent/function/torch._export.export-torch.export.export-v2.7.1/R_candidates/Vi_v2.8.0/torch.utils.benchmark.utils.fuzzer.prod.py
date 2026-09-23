def prod(values, base=1):
    """np.prod can overflow, so for sizes the product should be done in Python.

    Even though np.prod type promotes to int64, it can still overflow in which
    case the negative value will pass the size check and OOM when attempting to
    actually allocate the Tensor.
    """
    return functools.reduce(lambda x, y: int(x) * int(y), values, base)
