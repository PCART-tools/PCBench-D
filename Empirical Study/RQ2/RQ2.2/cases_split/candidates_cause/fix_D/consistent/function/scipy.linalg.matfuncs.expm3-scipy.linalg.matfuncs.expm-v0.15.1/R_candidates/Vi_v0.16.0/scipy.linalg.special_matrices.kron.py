def kron(a, b):
    """
    Kronecker product.

    The result is the block matrix::

        a[0,0]*b    a[0,1]*b  ... a[0,-1]*b
        a[1,0]*b    a[1,1]*b  ... a[1,-1]*b
        ...
        a[-1,0]*b   a[-1,1]*b ... a[-1,-1]*b

    Parameters
    ----------
    a : (M, N) ndarray
        Input array
    b : (P, Q) ndarray
        Input array

    Returns
    -------
    A : (M*P, N*Q) ndarray
        Kronecker product of `a` and `b`.

    Examples
    --------
    >>> from numpy import array
    >>> from scipy.linalg import kron
    >>> kron(array([[1,2],[3,4]]), array([[1,1,1]]))
    array([[1, 1, 1, 2, 2, 2],
           [3, 3, 3, 4, 4, 4]])

    """
    if not a.flags['CONTIGUOUS']:
        a = np.reshape(a, a.shape)
    if not b.flags['CONTIGUOUS']:
        b = np.reshape(b, b.shape)
    o = np.outer(a, b)
    o = o.reshape(a.shape + b.shape)
    return np.concatenate(np.concatenate(o, axis=1), axis=1)
