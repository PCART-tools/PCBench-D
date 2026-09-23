def tri(N, M=None, k=0, dtype=None):
    """
    Construct (N, M) matrix filled with ones at and below the k-th diagonal.

    The matrix has A[i,j] == 1 for i <= j + k

    Parameters
    ----------
    N : integer
        The size of the first dimension of the matrix.
    M : integer or None
        The size of the second dimension of the matrix. If `M` is None,
        `M = N` is assumed.
    k : integer
        Number of subdiagonal below which matrix is filled with ones.
        `k` = 0 is the main diagonal, `k` < 0 subdiagonal and `k` > 0
        superdiagonal.
    dtype : dtype
        Data type of the matrix.

    Returns
    -------
    tri : (N, M) ndarray
        Tri matrix.

    Examples
    --------
    >>> from scipy.linalg import tri
    >>> tri(3, 5, 2, dtype=int)
    array([[1, 1, 1, 0, 0],
           [1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1]])
    >>> tri(3, 5, -1, dtype=int)
    array([[0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0],
           [1, 1, 0, 0, 0]])

    """
    if M is None:
        M = N
    if isinstance(M, string_types):
        #pearu: any objections to remove this feature?
        #       As tri(N,'d') is equivalent to tri(N,dtype='d')
        dtype = M
        M = N
    m = np.greater_equal(np.subtract.outer(np.arange(N), np.arange(M)), -k)
    if dtype is None:
        return m
    else:
        return m.astype(dtype)
