def qz(A, B, output='real', lwork=None, sort=None, overwrite_a=False,
       overwrite_b=False, check_finite=True):
    """
    QZ decomposition for generalized eigenvalues of a pair of matrices.

    The QZ, or generalized Schur, decomposition for a pair of N x N
    nonsymmetric matrices (A,B) is::

        (A,B) = (Q*AA*Z', Q*BB*Z')

    where AA, BB is in generalized Schur form if BB is upper-triangular
    with non-negative diagonal and AA is upper-triangular, or for real QZ
    decomposition (``output='real'``) block upper triangular with 1x1
    and 2x2 blocks.  In this case, the 1x1 blocks correspond to real
    generalized eigenvalues and 2x2 blocks are 'standardized' by making
    the corresponding elements of BB have the form::

        [ a 0 ]
        [ 0 b ]

    and the pair of corresponding 2x2 blocks in AA and BB will have a complex
    conjugate pair of generalized eigenvalues.  If (``output='complex'``) or
    A and B are complex matrices, Z' denotes the conjugate-transpose of Z.
    Q and Z are unitary matrices.

    Parameters
    ----------
    A : (N, N) array_like
        2d array to decompose
    B : (N, N) array_like
        2d array to decompose
    output : {'real', 'complex'}, optional
        Construct the real or complex QZ decomposition for real matrices.
        Default is 'real'.
    lwork : int, optional
        Work array size.  If None or -1, it is automatically computed.
    sort : {None, callable, 'lhp', 'rhp', 'iuc', 'ouc'}, optional
        NOTE: THIS INPUT IS DISABLED FOR NOW. Use ordqz instead.

        Specifies whether the upper eigenvalues should be sorted.  A callable
        may be passed that, given a eigenvalue, returns a boolean denoting
        whether the eigenvalue should be sorted to the top-left (True). For
        real matrix pairs, the sort function takes three real arguments
        (alphar, alphai, beta). The eigenvalue
        ``x = (alphar + alphai*1j)/beta``.  For complex matrix pairs or
        output='complex', the sort function takes two complex arguments
        (alpha, beta). The eigenvalue ``x = (alpha/beta)``.  Alternatively,
        string parameters may be used:

            - 'lhp'   Left-hand plane (x.real < 0.0)
            - 'rhp'   Right-hand plane (x.real > 0.0)
            - 'iuc'   Inside the unit circle (x*x.conjugate() < 1.0)
            - 'ouc'   Outside the unit circle (x*x.conjugate() > 1.0)

        Defaults to None (no sorting).
    overwrite_a : bool, optional
        Whether to overwrite data in a (may improve performance)
    overwrite_b : bool, optional
        Whether to overwrite data in b (may improve performance)
    check_finite : bool, optional
        If true checks the elements of `A` and `B` are finite numbers. If
        false does no checking and passes matrix through to
        underlying algorithm.

    Returns
    -------
    AA : (N, N) ndarray
        Generalized Schur form of A.
    BB : (N, N) ndarray
        Generalized Schur form of B.
    Q : (N, N) ndarray
        The left Schur vectors.
    Z : (N, N) ndarray
        The right Schur vectors.

    Notes
    -----
    Q is transposed versus the equivalent function in Matlab.

    .. versionadded:: 0.11.0

    Examples
    --------
    >>> from scipy import linalg
    >>> np.random.seed(1234)
    >>> A = np.arange(9).reshape((3, 3))
    >>> B = np.random.randn(3, 3)

    >>> AA, BB, Q, Z = linalg.qz(A, B)
    >>> AA
    array([[-13.40928183,  -4.62471562,   1.09215523],
           [  0.        ,   0.        ,   1.22805978],
           [  0.        ,   0.        ,   0.31973817]])
    >>> BB
    array([[ 0.33362547, -1.37393632,  0.02179805],
           [ 0.        ,  1.68144922,  0.74683866],
           [ 0.        ,  0.        ,  0.9258294 ]])
    >>> Q
    array([[ 0.14134727, -0.97562773,  0.16784365],
           [ 0.49835904, -0.07636948, -0.86360059],
           [ 0.85537081,  0.20571399,  0.47541828]])
    >>> Z
    array([[-0.24900855, -0.51772687,  0.81850696],
           [-0.79813178,  0.58842606,  0.12938478],
           [-0.54861681, -0.6210585 , -0.55973739]])

    See also
    --------
    ordqz
    """
    # output for real
    # AA, BB, sdim, alphar, alphai, beta, vsl, vsr, work, info
    # output for complex
    # AA, BB, sdim, alpha, beta, vsl, vsr, work, info
    result, _ = _qz(A, B, output=output, lwork=lwork, sort=sort,
                    overwrite_a=overwrite_a, overwrite_b=overwrite_b,
                    check_finite=check_finite)
    return result[0], result[1], result[-4], result[-3]
