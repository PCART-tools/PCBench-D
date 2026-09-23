def _ip_hsd(A, b, c, c0, alpha0, beta, maxiter, disp, tol,
            sparse, lstsq, sym_pos, cholesky, pc, ip, permc_spec):
    r"""
    Solve a linear programming problem in standard form:

    minimize:     c'^T * x'

    subject to:   A * x' == b
                  0 < x' < oo

    using the interior point method of [1].

    Parameters
    ----------
    A : 2-D array
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the equality constraints at ``x`` (for standard form problem).
    b : 1-D array
        1-D array of values representing the RHS of each equality constraint
        (row) in ``A`` (for standard form problem).
    c : 1-D array
        Coefficients of the linear objective function to be minimized (for
        standard form problem).
    c0 : float
        Constant term in objective function due to fixed (and eliminated)
        variables. (Purely for display.)
    alpha0 : float
        The maximal step size for Mehrota's predictor-corrector search
        direction; see :math:`\beta_3`of [1] Table 8.1
    beta : float
        The desired reduction of the path parameter :math:`\mu` (see  [3]_)
    maxiter : int
        The maximum number of iterations of the algorithm.
    disp : bool
        Set to ``True`` if indicators of optimization status are to be printed
        to the console each iteration.
    tol : float
        Termination tolerance; see [1]_ Section 4.5.
    sparse : bool
        Set to ``True`` if the problem is to be treated as sparse. However,
        the inputs ``A_eq`` and ``A_ub`` should nonetheless be provided as
        (dense) arrays rather than sparse matrices.
    lstsq : bool
        Set to ``True`` if the problem is expected to be very poorly
        conditioned. This should always be left as ``False`` unless severe
        numerical difficulties are frequently encountered, and a better option
        would be to improve the formulation of the problem.
    sym_pos : bool
        Leave ``True`` if the problem is expected to yield a well conditioned
        symmetric positive definite normal equation matrix (almost always).
    cholesky : bool
        Set to ``True`` if the normal equations are to be solved by explicit
        Cholesky decomposition followed by explicit forward/backward
        substitution. This is typically faster for moderate, dense problems
        that are numerically well-behaved.
    pc : bool
        Leave ``True`` if the predictor-corrector method of Mehrota is to be
        used. This is almost always (if not always) beneficial.
    ip : bool
        Set to ``True`` if the improved initial point suggestion due to [1]_
        Section 4.3 is desired. It's unclear whether this is beneficial.
    permc_spec : str (default = 'MMD_AT_PLUS_A')
        (Has effect only with ``sparse = True``, ``lstsq = False``, ``sym_pos =
        True``.) A matrix is factorized in each iteration of the algorithm.
        This option specifies how to permute the columns of the matrix for
        sparsity preservation. Acceptable values are:

        - ``NATURAL``: natural ordering.
        - ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
        - ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
        - ``COLAMD``: approximate minimum degree column ordering.

        This option can impact the convergence of the
        interior point algorithm; test different values to determine which
        performs best for your problem. For more information, refer to
        ``scipy.sparse.linalg.splu``.

    Returns
    -------
    x_hat : float
        Solution vector (for standard form problem).
    status : int
        An integer representing the exit status of the optimization::

         0 : Optimization terminated successfully
         1 : Iteration limit reached
         2 : Problem appears to be infeasible
         3 : Problem appears to be unbounded
         4 : Serious numerical difficulties encountered.

    message : str
        A string descriptor of the exit status of the optimization.
    iteration : int
        The number of iterations taken to solve the problem

    References
    ----------
    .. [1] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.
    .. [3] Freund, Robert M. "Primal-Dual Interior-Point Methods for Linear
           Programming based on Newton's Method." Unpublished Course Notes,
           March 2004. Available 2/25/2017 at:
           https://ocw.mit.edu/courses/sloan-school-of-management/15-084j-nonlinear-programming-spring-2004/lecture-notes/lec14_int_pt_mthd.pdf

    """

    iteration = 0

    # default initial point
    x, y, z, tau, kappa = _get_blind_start(A.shape)

    # first iteration is special improvement of initial point
    ip = ip if pc else False

    # [1] 4.5
    rho_p, rho_d, rho_A, rho_g, rho_mu, obj = _indicators(
        A, b, c, c0, x, y, z, tau, kappa)
    go = rho_p > tol or rho_d > tol or rho_A > tol  # we might get lucky : )

    if disp:
        _display_iter(rho_p, rho_d, rho_g, "-", rho_mu, obj, header=True)

    status = 0
    message = "Optimization terminated successfully."

    if sparse:
        A = sps.csc_matrix(A)
        A.T = A.transpose()  # A.T is defined for sparse matrices but is slow
        # Redefine it to avoid calculating again
        # This is fine as long as A doesn't change

    while go:

        iteration += 1

        if ip:  # initial point
            # [1] Section 4.4
            gamma = 1

            def eta(g):
                return 1
        else:
            # gamma = 0 in predictor step according to [1] 4.1
            # if predictor/corrector is off, use mean of complementarity [3]
            # 5.1 / [4] Below Figure 10-4
            gamma = 0 if pc else beta * np.mean(z * x)
            # [1] Section 4.1

            def eta(g=gamma):
                return 1 - g

        try:
            # Solve [1] 8.6 and 8.7/8.13/8.23
            d_x, d_y, d_z, d_tau, d_kappa = _get_delta(
                A, b, c, x, y, z, tau, kappa, gamma, eta,
                sparse, lstsq, sym_pos, cholesky, pc, ip, permc_spec)

            if ip:  # initial point
                # [1] 4.4
                # Formula after 8.23 takes a full step regardless if this will
                # take it negative
                alpha = 1.0
                x, y, z, tau, kappa = _do_step(
                    x, y, z, tau, kappa, d_x, d_y,
                    d_z, d_tau, d_kappa, alpha)
                x[x < 1] = 1
                z[z < 1] = 1
                tau = max(1, tau)
                kappa = max(1, kappa)
                ip = False  # done with initial point
            else:
                # [1] Section 4.3
                alpha = _get_step(x, d_x, z, d_z, tau,
                                  d_tau, kappa, d_kappa, alpha0)
                # [1] Equation 8.9
                x, y, z, tau, kappa = _do_step(
                    x, y, z, tau, kappa, d_x, d_y, d_z, d_tau, d_kappa, alpha)

        except (LinAlgError, FloatingPointError):
            # this can happen when sparse solver is used and presolve
            # is turned off. I've never seen it otherwise.
            status = 4
            message = _get_message(status)
            break

        # [1] 4.5
        rho_p, rho_d, rho_A, rho_g, rho_mu, obj = _indicators(
            A, b, c, c0, x, y, z, tau, kappa)
        go = rho_p > tol or rho_d > tol or rho_A > tol

        if disp:
            _display_iter(rho_p, rho_d, rho_g, alpha, float(rho_mu), obj)

        # [1] 4.5
        inf1 = (rho_p < tol and rho_d < tol and rho_g < tol and tau < tol *
                max(1, kappa))
        inf2 = rho_mu < tol and tau < tol * min(1, kappa)
        if inf1 or inf2:
            # [1] Lemma 8.4 / Theorem 8.3
            if b.transpose().dot(y) > tol:
                status = 2
            else:  # elif c.T.dot(x) < tol: ? Probably not necessary.
                status = 3
            message = _get_message(status)
            break
        elif iteration >= maxiter:
            status = 1
            message = _get_message(status)
            break

    if disp:
        print(message)

    x_hat = x / tau
    # [1] Statement after Theorem 8.2
    return x_hat, status, message, iteration
