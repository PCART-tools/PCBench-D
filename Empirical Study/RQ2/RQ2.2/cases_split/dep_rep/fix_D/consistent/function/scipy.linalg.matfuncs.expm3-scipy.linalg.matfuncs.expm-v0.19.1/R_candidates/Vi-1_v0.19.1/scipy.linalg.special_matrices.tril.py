def tril(m, k=0):
    """
    Make a copy of a matrix with elements above the k-th diagonal zeroed.

    Parameters
    ----------
    m : array_like
        Matrix whose elements to return
    k : int, optional
        Diagonal above which to zero elements.
        `k` == 0 is the main diagonal, `k` < 0 subdiagonal and
        `k` > 0 superdiagonal.

    Returns
    -------
    tril : ndarray
        Return is the same shape and type as `m`.

    Examples
    --------
    >>> from scipy.linalg import tril
    >>> tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 0,  0,  0],
           [ 4,  0,  0],
           [ 7,  8,  0],
           [10, 11, 12]])

    """
    m = np.asarray(m)
    out = tri(m.shape[0], m.shape[1], k=k, dtype=m.dtype.char) * m
    return out
