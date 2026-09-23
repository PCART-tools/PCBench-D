def solve_continuous_are(a, b, q, r):
    """
    Solves the continuous algebraic Riccati equation, or CARE, defined
    as (A'X + XA - XBR^-1B'X+Q=0) directly using a Schur decomposition
    method.

    Parameters
    ----------
    a : (M, M) array_like
        Input
    b : (M, N) array_like
        Input
    q : (M, M) array_like
        Input
    r : (N, N) array_like
        Non-singular, square matrix

    Returns
    -------
    x : (M, M) ndarray
        Solution to the continuous algebraic Riccati equation

    See Also
    --------
    solve_discrete_are : Solves the discrete algebraic Riccati equation

    Notes
    -----
    Method taken from:
    Laub, "A Schur Method for Solving Algebraic Riccati Equations."
    U.S. Energy Research and Development Agency under contract
    ERDA-E(49-18)-2087.
    http://dspace.mit.edu/bitstream/handle/1721.1/1301/R-0859-05666488.pdf

    .. versionadded:: 0.11.0

    """

    try:
        g = inv(r)
    except LinAlgError:
        raise ValueError('Matrix R in the algebraic Riccati equation solver is ill-conditioned')

    g = np.dot(np.dot(b, g), b.conj().transpose())

    z11 = a
    z12 = -1.0*g
    z21 = -1.0*q
    z22 = -1.0*a.conj().transpose()

    z = np.vstack((np.hstack((z11, z12)), np.hstack((z21, z22))))

    # Note: we need to sort the upper left of s to have negative real parts,
    #       while the lower right is positive real components (Laub, p. 7)
    [s, u, sorted] = schur(z, sort='lhp')

    (m, n) = u.shape

    u11 = u[0:m//2, 0:n//2]
    u21 = u[m//2:m, 0:n//2]
    u11i = inv(u11)

    return np.dot(u21, u11i)
