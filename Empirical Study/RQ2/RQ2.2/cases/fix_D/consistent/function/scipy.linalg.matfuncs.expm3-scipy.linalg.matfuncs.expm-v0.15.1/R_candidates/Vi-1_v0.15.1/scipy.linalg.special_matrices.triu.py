def triu(m, k=0):
    """
    Make a copy of a matrix with elements below the k-th diagonal zeroed.

    Parameters
    ----------
    m : array_like
        Matrix whose elements to return
    k : int, optional
        Diagonal below which to zero elements.
        `k` == 0 is the main diagonal, `k` < 0 subdiagonal and
        `k` > 0 superdiagonal.

    Returns
    -------
    triu : ndarray
        Return matrix with zeroed elements below the k-th diagonal and has
        same shape and type as `m`.

    Examples
    --------
    >>> from scipy.linalg import triu
    >>> triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]])

    """
    m = np.asarray(m)
    out = (1 - tri(m.shape[0], m.shape[1], k - 1, m.dtype.char)) * m
    return out
