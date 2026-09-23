def argsreduce(cond, *args):
    """Return the sequence of ravel(args[i]) where ravel(condition) is
    True in 1D.

    Examples
    --------
    >>> import numpy as np
    >>> rand = np.random.random_sample
    >>> A = rand((4,5))
    >>> B = 2
    >>> C = rand((1,5))
    >>> cond = np.ones(A.shape)
    >>> [A1,B1,C1] = argsreduce(cond,A,B,C)
    >>> B1.shape
    (20,)
    >>> cond[2,:] = 0
    >>> [A2,B2,C2] = argsreduce(cond,A,B,C)
    >>> B2.shape
    (15,)

    """
    newargs = atleast_1d(*args)
    if not isinstance(newargs, list):
        newargs = [newargs,]
    expand_arr = (cond == cond)
    return [extract(cond, arr1 * expand_arr) for arr1 in newargs]
