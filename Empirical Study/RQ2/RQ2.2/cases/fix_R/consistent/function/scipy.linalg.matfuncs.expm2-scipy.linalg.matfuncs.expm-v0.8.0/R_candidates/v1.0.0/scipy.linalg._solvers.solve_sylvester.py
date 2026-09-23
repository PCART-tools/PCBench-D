def solve_sylvester(a, b, q):
    """
    Computes a solution (X) to the Sylvester equation :math:`AX + XB = Q`.

    Parameters
    ----------
    a : (M, M) array_like
        Leading matrix of the Sylvester equation
    b : (N, N) array_like
        Trailing matrix of the Sylvester equation
    q : (M, N) array_like
        Right-hand side

    Returns
    -------
    x : (M, N) ndarray
        The solution to the Sylvester equation.

    Raises
    ------
    LinAlgError
        If solution was not found

    Notes
    -----
    Computes a solution to the Sylvester matrix equation via the Bartels-
    Stewart algorithm.  The A and B matrices first undergo Schur
    decompositions.  The resulting matrices are used to construct an
    alternative Sylvester equation (``RY + YS^T = F``) where the R and S
    matrices are in quasi-triangular form (or, when R, S or F are complex,
    triangular form).  The simplified equation is then solved using
    ``*TRSYL`` from LAPACK directly.

    .. versionadded:: 0.11.0

    Examples
    --------
    Given `a`, `b`, and `q` solve for `x`:

    >>> from scipy import linalg
    >>> a = np.array([[-3, -2, 0], [-1, -1, 3], [3, -5, -1]])
    >>> b = np.array([[1]])
    >>> q = np.array([[1],[2],[3]])
    >>> x = linalg.solve_sylvester(a, b, q)
    >>> x
    array([[ 0.0625],
           [-0.5625],
           [ 0.6875]])
    >>> np.allclose(a.dot(x) + x.dot(b), q)
    True

    """

    # Compute the Schur decomp form of a
    r, u = schur(a, output='real')

    # Compute the Schur decomp of b
    s, v = schur(b.conj().transpose(), output='real')

    # Construct f = u'*q*v
    f = np.dot(np.dot(u.conj().transpose(), q), v)

    # Call the Sylvester equation solver
    trsyl, = get_lapack_funcs(('trsyl',), (r, s, f))
    if trsyl is None:
        raise RuntimeError('LAPACK implementation does not contain a proper '
                           'Sylvester equation solver (TRSYL)')
    y, scale, info = trsyl(r, s, f, tranb='C')

    y = scale*y

    if info < 0:
        raise LinAlgError("Illegal value encountered in "
                          "the %d term" % (-info,))

    return np.dot(np.dot(u, y), v.conj().transpose())
