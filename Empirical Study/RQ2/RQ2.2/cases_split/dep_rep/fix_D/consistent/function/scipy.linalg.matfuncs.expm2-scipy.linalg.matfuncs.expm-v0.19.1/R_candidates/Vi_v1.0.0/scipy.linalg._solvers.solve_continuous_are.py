def solve_continuous_are(a, b, q, r, e=None, s=None, balanced=True):
    r"""
    Solves the continuous-time algebraic Riccati equation (CARE).

    The CARE is defined as

    .. math::

          X A + A^H X - X B R^{-1} B^H X + Q = 0

    The limitations for a solution to exist are :

        * All eigenvalues of :math:`A` on the right half plane, should be
          controllable.

        * The associated hamiltonian pencil (See Notes), should have
          eigenvalues sufficiently away from the imaginary axis.

    Moreover, if ``e`` or ``s`` is not precisely ``None``, then the
    generalized version of CARE

    .. math::

          E^HXA + A^HXE - (E^HXB + S) R^{-1} (B^HXE + S^H) + Q = 0

    is solved. When omitted, ``e`` is assumed to be the identity and ``s``
    is assumed to be the zero matrix with sizes compatible with ``a`` and
    ``b`` respectively.

    Parameters
    ----------
    a : (M, M) array_like
        Square matrix
    b : (M, N) array_like
        Input
    q : (M, M) array_like
        Input
    r : (N, N) array_like
        Nonsingular square matrix
    e : (M, M) array_like, optional
        Nonsingular square matrix
    s : (M, N) array_like, optional
        Input
    balanced : bool, optional
        The boolean that indicates whether a balancing step is performed
        on the data. The default is set to True.

    Returns
    -------
    x : (M, M) ndarray
        Solution to the continuous-time algebraic Riccati equation.

    Raises
    ------
    LinAlgError
        For cases where the stable subspace of the pencil could not be
        isolated. See Notes section and the references for details.

    See Also
    --------
    solve_discrete_are : Solves the discrete-time algebraic Riccati equation

    Notes
    -----
    The equation is solved by forming the extended hamiltonian matrix pencil,
    as described in [1]_, :math:`H - \lambda J` given by the block matrices ::

        [ A    0    B ]             [ E   0    0 ]
        [-Q  -A^H  -S ] - \lambda * [ 0  E^H   0 ]
        [ S^H B^H   R ]             [ 0   0    0 ]

    and using a QZ decomposition method.

    In this algorithm, the fail conditions are linked to the symmetry
    of the product :math:`U_2 U_1^{-1}` and condition number of
    :math:`U_1`. Here, :math:`U` is the 2m-by-m matrix that holds the
    eigenvectors spanning the stable subspace with 2m rows and partitioned
    into two m-row matrices. See [1]_ and [2]_ for more details.

    In order to improve the QZ decomposition accuracy, the pencil goes
    through a balancing step where the sum of absolute values of
    :math:`H` and :math:`J` entries (after removing the diagonal entries of
    the sum) is balanced following the recipe given in [3]_.

    .. versionadded:: 0.11.0

    References
    ----------
    .. [1]  P. van Dooren , "A Generalized Eigenvalue Approach For Solving
       Riccati Equations.", SIAM Journal on Scientific and Statistical
       Computing, Vol.2(2), DOI: 10.1137/0902010

    .. [2] A.J. Laub, "A Schur Method for Solving Algebraic Riccati
       Equations.", Massachusetts Institute of Technology. Laboratory for
       Information and Decision Systems. LIDS-R ; 859. Available online :
       http://hdl.handle.net/1721.1/1301

    .. [3] P. Benner, "Symplectic Balancing of Hamiltonian Matrices", 2001,
       SIAM J. Sci. Comput., 2001, Vol.22(5), DOI: 10.1137/S1064827500367993

    Examples
    --------
    Given `a`, `b`, `q`, and `r` solve for `x`:

    >>> from scipy import linalg
    >>> a = np.array([[4, 3], [-4.5, -3.5]])
    >>> b = np.array([[1], [-1]])
    >>> q = np.array([[9, 6], [6, 4.]])
    >>> r = 1
    >>> x = linalg.solve_continuous_are(a, b, q, r)
    >>> x
    array([[ 21.72792206,  14.48528137],
           [ 14.48528137,   9.65685425]])
    >>> np.allclose(a.T.dot(x) + x.dot(a)-x.dot(b).dot(b.T).dot(x), -q)
    True

    """

    # Validate input arguments
    a, b, q, r, e, s, m, n, r_or_c, gen_are = _are_validate_args(
                                                     a, b, q, r, e, s, 'care')

    H = np.empty((2*m+n, 2*m+n), dtype=r_or_c)
    H[:m, :m] = a
    H[:m, m:2*m] = 0.
    H[:m, 2*m:] = b
    H[m:2*m, :m] = -q
    H[m:2*m, m:2*m] = -a.conj().T
    H[m:2*m, 2*m:] = 0. if s is None else -s
    H[2*m:, :m] = 0. if s is None else s.conj().T
    H[2*m:, m:2*m] = b.conj().T
    H[2*m:, 2*m:] = r

    if gen_are and e is not None:
        J = block_diag(e, e.conj().T, np.zeros_like(r, dtype=r_or_c))
    else:
        J = block_diag(np.eye(2*m), np.zeros_like(r, dtype=r_or_c))

    if balanced:
        # xGEBAL does not remove the diagonals before scaling. Also
        # to avoid destroying the Symplectic structure, we follow Ref.3
        M = np.abs(H) + np.abs(J)
        M[np.diag_indices_from(M)] = 0.
        _, (sca, _) = matrix_balance(M, separate=1, permute=0)
        # do we need to bother?
        if not np.allclose(sca, np.ones_like(sca)):
            # Now impose diag(D,inv(D)) from Benner where D is
            # square root of s_i/s_(n+i) for i=0,....
            sca = np.log2(sca)
            # NOTE: Py3 uses "Bankers Rounding: round to the nearest even" !!
            s = np.round((sca[m:2*m] - sca[:m])/2)
            sca = 2 ** np.r_[s, -s, sca[2*m:]]
            # Elementwise multiplication via broadcasting.
            elwisescale = sca[:, None] * np.reciprocal(sca)
            H *= elwisescale
            J *= elwisescale

    # Deflate the pencil to 2m x 2m ala Ref.1, eq.(55)
    q, r = qr(H[:, -n:])
    H = q[:, n:].conj().T.dot(H[:, :2*m])
    J = q[:2*m, n:].conj().T.dot(J[:2*m, :2*m])

    # Decide on which output type is needed for QZ
    out_str = 'real' if r_or_c == float else 'complex'

    _, _, _, _, _, u = ordqz(H, J, sort='lhp', overwrite_a=True,
                             overwrite_b=True, check_finite=False,
                             output=out_str)

    # Get the relevant parts of the stable subspace basis
    if e is not None:
        u, _ = qr(np.vstack((e.dot(u[:m, :m]), u[m:, :m])))
    u00 = u[:m, :m]
    u10 = u[m:, :m]

    # Solve via back-substituion after checking the condition of u00
    up, ul, uu = lu(u00)
    if 1/cond(uu) < np.spacing(1.):
        raise LinAlgError('Failed to find a finite solution.')

    # Exploit the triangular structure
    x = solve_triangular(ul.conj().T,
                         solve_triangular(uu.conj().T,
                                          u10.conj().T,
                                          lower=True),
                         unit_diagonal=True,
                         ).conj().T.dot(up.conj().T)
    if balanced:
        x *= sca[:m, None] * sca[:m]

    # Check the deviation from symmetry for success
    u_sym = u00.conj().T.dot(u10)
    n_u_sym = norm(u_sym, 1)
    u_sym = u_sym - u_sym.conj().T
    sym_threshold = np.max([np.spacing(1000.), n_u_sym])

    if norm(u_sym, 1) > sym_threshold:
        raise LinAlgError('The associated Hamiltonian pencil has eigenvalues '
                          'too close to the imaginary axis')

    return (x + x.conj().T)/2
