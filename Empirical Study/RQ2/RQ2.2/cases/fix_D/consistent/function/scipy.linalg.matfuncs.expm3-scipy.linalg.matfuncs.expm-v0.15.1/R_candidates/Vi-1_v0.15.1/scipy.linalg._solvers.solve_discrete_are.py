def solve_discrete_are(a, b, q, r):
    """
    Solves the disctrete algebraic Riccati equation, or DARE, defined as
    (X = A'XA-(A'XB)(R+B'XB)^-1(B'XA)+Q), directly using a Schur decomposition
    method.

    Parameters
    ----------
    a : (M, M) array_like
        Non-singular, square matrix
    b : (M, N) array_like
        Input
    q : (M, M) array_like
        Input
    r : (N, N) array_like
        Non-singular, square matrix

    Returns
    -------
    x : ndarray
        Solution to the continuous Lyapunov equation

    See Also
    --------
    solve_continuous_are : Solves the continuous algebraic Riccati equation

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

    try:
        ait = inv(a).conj().transpose()  # ait is "A inverse transpose"
    except LinAlgError:
        raise ValueError('Matrix A in the algebraic Riccati equation solver is ill-conditioned')

    z11 = a+np.dot(np.dot(g, ait), q)
    z12 = -1.0*np.dot(g, ait)
    z21 = -1.0*np.dot(ait, q)
    z22 = ait

    z = np.vstack((np.hstack((z11, z12)), np.hstack((z21, z22))))

    # Note: we need to sort the upper left of s to lie within the unit circle,
    #       while the lower right is outside (Laub, p. 7)
    [s, u, sorted] = schur(z, sort='iuc')

    (m,n) = u.shape

    u11 = u[0:m//2, 0:n//2]
    u21 = u[m//2:m, 0:n//2]
    u11i = inv(u11)

    return np.dot(u21, u11i)
