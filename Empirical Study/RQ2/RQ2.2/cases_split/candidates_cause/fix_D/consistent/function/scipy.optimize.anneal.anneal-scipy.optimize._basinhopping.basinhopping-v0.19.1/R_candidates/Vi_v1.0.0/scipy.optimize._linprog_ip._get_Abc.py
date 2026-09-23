def _get_Abc(
        c,
        c0=0,
        A_ub=None,
        b_ub=None,
        A_eq=None,
        b_eq=None,
        bounds=None,
        undo=[]):
    """
    Given a linear programming problem of the form:

    minimize:     c^T * x

    subject to:   A_ub * x <= b_ub
                  A_eq * x == b_eq
                  bounds[i][0] < x_i < bounds[i][1]

    return the problem in standard form:
    minimize:     c'^T * x'

    subject to:   A * x' == b
                  0 < x' < oo

    by adding slack variables and making variable substitutions as necessary.

    Parameters
    ----------
    c : 1-D array
        Coefficients of the linear objective function to be minimized.
        Components corresponding with fixed variables have been eliminated.
    c0 : float
        Constant term in objective function due to fixed (and eliminated)
        variables.
    A_ub : 2-D array
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the upper-bound inequality constraints at ``x``. Unnecessary
        rows/columns have been removed.
    b_ub : 1-D array
        1-D array of values representing the upper-bound of each inequality
        constraint (row) in ``A_ub``. Unnecessary elements have been removed.
    A_eq : 2-D array
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the equality constraints at ``x``. Unnecessary rows/columns have been
        removed.
    b_eq : 1-D array
        1-D array of values representing the RHS of each equality constraint
        (row) in ``A_eq``. Unnecessary elements have been removed.
    bounds : sequence of tuples
        ``(min, max)`` pairs for each element in ``x``, defining
        the bounds on that parameter. Use None for each of ``min`` or
        ``max`` when there is no bound in that direction. Bounds have been
        tightened where possible.
    undo: list of tuples
        (`index`, `value`) pairs that record the original index and fixed value
        for each variable removed from the problem

    Returns
    -------
    A : 2-D array
        2-D array which, when matrix-multiplied by x, gives the values of the
        equality constraints at x (for standard form problem).
    b : 1-D array
        1-D array of values representing the RHS of each equality constraint
        (row) in A (for standard form problem).
    c : 1-D array
        Coefficients of the linear objective function to be minimized (for
        standard form problem).
    c0 : float
        Constant term in objective function due to fixed (and eliminated)
        variables.

    References
    ----------
    .. [6] Bertsimas, Dimitris, and J. Tsitsiklis. "Introduction to linear
           programming." Athena Scientific 1 (1997): 997.

    """

    if sps.issparse(A_eq):
        sparse = True
        A_eq = sps.lil_matrix(A_eq)
        A_ub = sps.lil_matrix(A_ub)

        def hstack(blocks):
            return sps.hstack(blocks, format="lil")

        def vstack(blocks):
            return sps.vstack(blocks, format="lil")

        zeros = sps.lil_matrix
        eye = sps.eye
    else:
        sparse = False
        hstack = np.hstack
        vstack = np.vstack
        zeros = np.zeros
        eye = np.eye

    fixed_x = set()
    if len(undo) > 0:
        # these are indices of variables removed from the problem
        # however, their bounds are still part of the bounds list
        fixed_x = set(undo[0])
    # they are needed elsewhere, but not here
    bounds = [bounds[i] for i in range(len(bounds)) if i not in fixed_x]
    # in retrospect, the standard form of bounds should have been an n x 2
    # array. maybe change it someday.

    # modify problem such that all variables have only non-negativity bounds

    bounds = np.array(bounds)
    lbs = bounds[:, 0]
    ubs = bounds[:, 1]
    m_ub, n_ub = A_ub.shape

    lb_none = np.equal(lbs, None)
    ub_none = np.equal(ubs, None)
    lb_some = np.logical_not(lb_none)
    ub_some = np.logical_not(ub_none)

    # if preprocessing is on, lb == ub can't happen
    # if preprocessing is off, then it would be best to convert that
    # to an equality constraint, but it's tricky to make the other
    # required modifications from inside here.

    # unbounded below: substitute xi = -xi' (unbounded above)
    l_nolb_someub = np.logical_and(lb_none, ub_some)
    i_nolb = np.where(l_nolb_someub)[0]
    lbs[l_nolb_someub], ubs[l_nolb_someub] = (
        -ubs[l_nolb_someub], lbs[l_nolb_someub])
    lb_none = np.equal(lbs, None)
    ub_none = np.equal(ubs, None)
    lb_some = np.logical_not(lb_none)
    ub_some = np.logical_not(ub_none)
    c[i_nolb] *= -1
    if len(i_nolb) > 0:
        if A_ub.shape[0] > 0:  # sometimes needed for sparse arrays... weird
            A_ub[:, i_nolb] *= -1
        if A_eq.shape[0] > 0:
            A_eq[:, i_nolb] *= -1

    # upper bound: add inequality constraint
    i_newub = np.where(ub_some)[0]
    ub_newub = ubs[ub_some]
    n_bounds = np.count_nonzero(ub_some)
    A_ub = vstack((A_ub, zeros((n_bounds, A_ub.shape[1]))))
    b_ub = np.concatenate((b_ub, np.zeros(n_bounds)))
    A_ub[range(m_ub, A_ub.shape[0]), i_newub] = 1
    b_ub[m_ub:] = ub_newub

    A1 = vstack((A_ub, A_eq))
    b = np.concatenate((b_ub, b_eq))
    c = np.concatenate((c, np.zeros((A_ub.shape[0],))))

    # unbounded: substitute xi = xi+ + xi-
    l_free = np.logical_and(lb_none, ub_none)
    i_free = np.where(l_free)[0]
    n_free = len(i_free)
    A1 = hstack((A1, zeros((A1.shape[0], n_free))))
    c = np.concatenate((c, np.zeros(n_free)))
    A1[:, range(n_ub, A1.shape[1])] = -A1[:, i_free]
    c[np.arange(n_ub, A1.shape[1])] = -c[i_free]

    # add slack variables
    A2 = vstack([eye(A_ub.shape[0]), zeros((A_eq.shape[0], A_ub.shape[0]))])
    A = hstack([A1, A2])

    # lower bound: substitute xi = xi' + lb
    # now there is a constant term in objective
    i_shift = np.where(lb_some)[0]
    lb_shift = lbs[lb_some].astype(float)
    c0 += np.sum(lb_shift * c[i_shift])
    if sparse:
        b = b.reshape(-1, 1)
        A = A.tocsc()
        b -= (A[:, i_shift] * sps.diags(lb_shift)).sum(axis=1)
        b = b.ravel()
    else:
        b -= (A[:, i_shift] * lb_shift).sum(axis=1)

    return A, b, c, c0
