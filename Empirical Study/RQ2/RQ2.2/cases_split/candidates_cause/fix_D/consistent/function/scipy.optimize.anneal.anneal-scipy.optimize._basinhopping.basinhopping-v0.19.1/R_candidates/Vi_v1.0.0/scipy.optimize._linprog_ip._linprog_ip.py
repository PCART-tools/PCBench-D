def _linprog_ip(
        c,
        A_ub=None,
        b_ub=None,
        A_eq=None,
        b_eq=None,
        bounds=None,
        callback=None,
        alpha0=.99995,
        beta=0.1,
        maxiter=1000,
        disp=False,
        tol=1e-8,
        sparse=False,
        lstsq=False,
        sym_pos=True,
        cholesky=None,
        pc=True,
        ip=False,
        presolve=True,
        permc_spec='MMD_AT_PLUS_A',
        rr=True,
        _sparse_presolve=False,
        **unknown_options):
    r"""
    Minimize a linear objective function subject to linear
    equality constraints, linear inequality constraints, and simple bounds
    using the interior point method of [1]_.

    Linear programming is intended to solve problems of the following form::

        Minimize:     c^T * x

        Subject to:   A_ub * x <= b_ub
                      A_eq * x == b_eq
                      bounds[i][0] < x_i < bounds[i][1]

    Parameters
    ----------
    c : array_like
        Coefficients of the linear objective function to be minimized.
    A_ub : array_like, optional
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the upper-bound inequality constraints at ``x``.
    b_ub : array_like, optional
        1-D array of values representing the upper-bound of each inequality
        constraint (row) in ``A_ub``.
    A_eq : array_like, optional
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the equality constraints at ``x``.
    b_eq : array_like, optional
        1-D array of values representing the right hand side of each equality
        constraint (row) in ``A_eq``.
    bounds : sequence, optional
        ``(min, max)`` pairs for each element in ``x``, defining
        the bounds on that parameter. Use ``None`` for one of ``min`` or
        ``max`` when there is no bound in that direction. By default
        bounds are ``(0, None)`` (non-negative).
        If a sequence containing a single tuple is provided, then ``min`` and
        ``max`` will be applied to all variables in the problem.

    Options
    -------
    maxiter : int (default = 1000)
        The maximum number of iterations of the algorithm.
    disp : bool (default = False)
        Set to ``True`` if indicators of optimization status are to be printed
        to the console each iteration.
    tol : float (default = 1e-8)
        Termination tolerance to be used for all termination criteria;
        see [1]_ Section 4.5.
    alpha0 : float (default = 0.99995)
        The maximal step size for Mehrota's predictor-corrector search
        direction; see :math:`\beta_{3}` of [1]_ Table 8.1.
    beta : float (default = 0.1)
        The desired reduction of the path parameter :math:`\mu` (see [3]_)
        when Mehrota's predictor-corrector is not in use (uncommon).
    sparse : bool (default = False)
        Set to ``True`` if the problem is to be treated as sparse after
        presolve. If either ``A_eq`` or ``A_ub`` is a sparse matrix,
        this option will automatically be set ``True``, and the problem
        will be treated as sparse even during presolve. If your constraint
        matrices contain mostly zeros and the problem is not very small (less
        than about 100 constraints or variables), consider setting ``True``
        or providing ``A_eq`` and ``A_ub`` as sparse matrices.
    lstsq : bool (default = False)
        Set to ``True`` if the problem is expected to be very poorly
        conditioned. This should always be left ``False`` unless severe
        numerical difficulties are encountered. Leave this at the default
        unless you receive a warning message suggesting otherwise.
    sym_pos : bool (default = True)
        Leave ``True`` if the problem is expected to yield a well conditioned
        symmetric positive definite normal equation matrix
        (almost always). Leave this at the default unless you receive
        a warning message suggesting otherwise.
    cholesky : bool (default = True)
        Set to ``True`` if the normal equations are to be solved by explicit
        Cholesky decomposition followed by explicit forward/backward
        substitution. This is typically faster for moderate, dense problems
        that are numerically well-behaved.
    pc : bool (default = True)
        Leave ``True`` if the predictor-corrector method of Mehrota is to be
        used. This is almost always (if not always) beneficial.
    ip : bool (default = False)
        Set to ``True`` if the improved initial point suggestion due to [1]_
        Section 4.3 is desired. Whether this is beneficial or not
        depends on the problem.
    presolve : bool (default = True)
        Leave ``True`` if presolve routine should be run. The presolve routine
        is almost always useful because it can detect trivial infeasibilities
        and unboundedness, eliminate fixed variables, and remove redundancies.
        One circumstance in which it might be turned off (set ``False``) is
        when it detects that the problem is trivially unbounded; it is possible
        that that the problem is truly infeasibile but this has not been
        detected.
    rr : bool (default = True)
        Default ``True`` attempts to eliminate any redundant rows in ``A_eq``.
        Set ``False`` if ``A_eq`` is known to be of full row rank, or if you
        are looking for a potential speedup (at the expense of reliability).
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
    A ``scipy.optimize.OptimizeResult`` consisting of the following fields:

        x : ndarray
            The independent variable vector which optimizes the linear
            programming problem.
        fun : float
            The optimal value of the objective function
        con : float
            The residuals of the equality constraints (nominally zero).
        slack : ndarray
            The values of the slack variables.  Each slack variable corresponds
            to an inequality constraint.  If the slack is zero, then the
            corresponding constraint is active.
        success : bool
            Returns True if the algorithm succeeded in finding an optimal
            solution.
        status : int
            An integer representing the exit status of the optimization::

                 0 : Optimization terminated successfully
                 1 : Iteration limit reached
                 2 : Problem appears to be infeasible
                 3 : Problem appears to be unbounded
                 4 : Serious numerical difficulties encountered

        nit : int
            The number of iterations performed.
        message : str
            A string descriptor of the exit status of the optimization.

    Notes
    -----

    This method implements the algorithm outlined in [1]_ with ideas from [5]_
    and a structure inspired by the simpler methods of [3]_ and [4]_.

    First, a presolve procedure based on [5]_ attempts to identify trivial
    infeasibilities, trivial unboundedness, and potential problem
    simplifications. Specifically, it checks for:

    - rows of zeros in ``A_eq`` or ``A_ub``, representing trivial constraints;
    - columns of zeros in ``A_eq`` `and` ``A_ub``, representing unconstrained
      variables;
    - column singletons in ``A_eq``, representing fixed variables; and
    - column singletons in ``A_ub``, representing simple bounds.

    If presolve reveals that the problem is unbounded (e.g. an unconstrained
    and unbounded variable has negative cost) or infeasible (e.g. a row of
    zeros in ``A_eq`` corresponds with a nonzero in ``b_eq``), the solver
    terminates with the appropriate status code. Note that presolve terminates
    as soon as any sign of unboundedness is detected; consequently, a problem
    may be reported as unbounded when in reality the problem is infeasible
    (but infeasibility has not been detected yet). Therefore, if the output
    message states that unboundedness is detected in presolve and it is
    necessary to know whether the problem is actually infeasible, set option
    ``presolve=False``.

    If neither infeasibility nor unboundedness are detected in a single pass
    of the presolve check, bounds are tightened where possible and fixed
    variables are removed from the problem. Then, linearly dependent rows
    of the ``A_eq`` matrix are removed, (unless they represent an
    infeasibility) to avoid numerical difficulties in the primary solve
    routine. Note that rows that are nearly linearly dependent (within a
    prescibed tolerance) may also be removed, which can change the optimal
    solution in rare cases. If this is a concern, eliminate redundancy from
    your problem formulation and run with option ``rr=False`` or
    ``presolve=False``.

    Several potential improvements can be made here: additional presolve
    checks outlined in [5]_ should be implemented, the presolve routine should
    be run multiple times (until no further simplifications can be made), and
    more of the efficiency improvements from [2]_ should be implemented in the
    redundancy removal routines.

    After presolve, the problem is transformed to standard form by converting
    the (tightened) simple bounds to upper bound constraints, introducing
    non-negative slack variables for inequality constraints, and expressing
    unbounded variables as the difference between two non-negative variables.

    The primal-dual path following method begins with initial 'guesses' of
    the primal and dual variables of the standard form problem and iteratively
    attempts to solve the (nonlinear) Karush-Kuhn-Tucker conditions for the
    problem with a gradually reduced logarithmic barrier term added to the
    objective. This particular implementation uses a homogeneous self-dual
    formulation, which provides certificates of infeasibility or unboundedness
    where applicable.

    The default initial point for the primal and dual variables is that
    defined in [1]_ Section 4.4 Equation 8.22. Optionally (by setting initial
    point option ``ip=True``), an alternate (potentially improved) starting
    point can be calculated according to the additional recommendations of
    [1]_ Section 4.4.

    A search direction is calculated using the predictor-corrector method
    (single correction) proposed by Mehrota and detailed in [1]_ Section 4.1.
    (A potential improvement would be to implement the method of multiple
    corrections described in [1]_ Section 4.2.) In practice, this is
    accomplished by solving the normal equations, [1]_ Section 5.1 Equations
    8.31 and 8.32, derived from the Newton equations [1]_ Section 5 Equations
    8.25 (compare to [1]_ Section 4 Equations 8.6-8.8). The advantage of
    solving the normal equations rather than 8.25 directly is that the
    matrices involved are symmetric positive definite, so Cholesky
    decomposition can be used rather than the more expensive LU factorization.

    With the default ``cholesky=True``, this is accomplished using
    ``scipy.linalg.cho_factor`` followed by forward/backward substitutions
    via ``scipy.linalg.cho_solve``. With ``cholesky=False`` and
    ``sym_pos=True``, Cholesky decomposition is performed instead by
    ``scipy.linalg.solve``. Based on speed tests, this also appears to retain
    the Cholesky decomposition of the matrix for later use, which is beneficial
    as the same system is solved four times with different right hand sides
    in each iteration of the algorithm.

    In problems with redundancy (e.g. if presolve is turned off with option
    ``presolve=False``) or if the matrices become ill-conditioned (e.g. as the
    solution is approached and some decision variables approach zero),
    Cholesky decomposition can fail. Should this occur, successively more
    robust solvers (``scipy.linalg.solve`` with ``sym_pos=False`` then
    ``scipy.linalg.lstsq``) are tried, at the cost of computational efficiency.
    These solvers can be used from the outset by setting the options
    ``sym_pos=False`` and ``lstsq=True``, respectively.

    Note that with the option ``sparse=True``, the normal equations are solved
    using ``scipy.sparse.linalg.spsolve``. Unfortunately, this uses the more
    expensive LU decomposition from the outset, but for large, sparse problems,
    the use of sparse linear algebra techniques improves the solve speed
    despite the use of LU rather than Cholesky decomposition. A simple
    improvement would be to use the sparse Cholesky decomposition of
    ``CHOLMOD`` via ``scikit-sparse`` when available.

    Other potential improvements for combatting issues associated with dense
    columns in otherwise sparse problems are outlined in [1]_ Section 5.3 and
    [7]_ Section 4.1-4.2; the latter also discusses the alleviation of
    accuracy issues associated with the substitution approach to free
    variables.

    After calculating the search direction, the maximum possible step size
    that does not activate the non-negativity constraints is calculated, and
    the smaller of this step size and unity is applied (as in [1]_ Section
    4.1.) [1]_ Section 4.3 suggests improvements for choosing the step size.

    The new point is tested according to the termination conditions of [1]_
    Section 4.5. The same tolerance, which can be set using the ``tol`` option,
    is used for all checks. (A potential improvement would be to expose
    the different tolerances to be set independently.) If optimality,
    unboundedness, or infeasibility is detected, the solve procedure
    terminates; otherwise it repeats.

    If optimality is achieved, a postsolve procedure undoes transformations
    associated with presolve and converting to standard form. It then
    calculates the residuals (equality constraint violations, which should
    be very small) and slacks (difference between the left and right hand
    sides of the upper bound constraints) of the original problem, which are
    returned with the solution in an ``OptimizeResult`` object.

    References
    ----------
    .. [1] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.
    .. [2] Andersen, Erling D. "Finding all linearly dependent rows in
           large-scale linear programming." Optimization Methods and Software
           6.3 (1995): 219-227.
    .. [3] Freund, Robert M. "Primal-Dual Interior-Point Methods for Linear
           Programming based on Newton's Method." Unpublished Course Notes,
           March 2004. Available 2/25/2017 at
           https://ocw.mit.edu/courses/sloan-school-of-management/15-084j-nonlinear-programming-spring-2004/lecture-notes/lec14_int_pt_mthd.pdf
    .. [4] Fourer, Robert. "Solving Linear Programs by Interior-Point Methods."
           Unpublished Course Notes, August 26, 2005. Available 2/25/2017 at
           http://www.4er.org/CourseNotes/Book%20B/B-III.pdf
    .. [5] Andersen, Erling D., and Knud D. Andersen. "Presolving in linear
           programming." Mathematical Programming 71.2 (1995): 221-245.
    .. [6] Bertsimas, Dimitris, and J. Tsitsiklis. "Introduction to linear
           programming." Athena Scientific 1 (1997): 997.
    .. [7] Andersen, Erling D., et al. Implementation of interior point methods
           for large scale linear programming. HEC/Universite de Geneve, 1996.

    """

    _check_unknown_options(unknown_options)

    if callback is not None:
        raise NotImplementedError("method 'interior-point' does not support "
                                  "callback functions.")

    # This is an undocumented option for unit testing sparse presolve
    if _sparse_presolve and A_eq is not None:
        A_eq = sp.sparse.coo_matrix(A_eq)
    if _sparse_presolve and A_ub is not None:
        A_ub = sp.sparse.coo_matrix(A_ub)

    # These should be warnings, not errors
    if not sparse and (sp.sparse.issparse(A_eq) or sp.sparse.issparse(A_ub)):
        sparse = True
        warn("Sparse constraint matrix detected; setting 'sparse':True.",
             OptimizeWarning)

    if sparse and lstsq:
        warn("Invalid option combination 'sparse':True "
             "and 'lstsq':True; Sparse least squares is not recommended.",
             OptimizeWarning)

    if sparse and not sym_pos:
        warn("Invalid option combination 'sparse':True "
             "and 'sym_pos':False; the effect is the same as sparse least "
             "squares, which is not recommended.",
             OptimizeWarning)

    if sparse and cholesky:
        # Cholesky decomposition is not available for sparse problems
        warn("Invalid option combination 'sparse':True "
             "and 'cholesky':True; sparse Colesky decomposition is not "
             "available.",
             OptimizeWarning)

    if lstsq and cholesky:
        warn("Invalid option combination 'lstsq':True "
             "and 'cholesky':True; option 'cholesky' has no effect when "
             "'lstsq' is set True.",
             OptimizeWarning)

    valid_permc_spec = ('NATURAL', 'MMD_ATA', 'MMD_AT_PLUS_A', 'COLAMD')
    if permc_spec.upper() not in valid_permc_spec:
        warn("Invalid permc_spec option: '" + str(permc_spec) + "'. "
             "Acceptable values are 'NATURAL', 'MMD_ATA', 'MMD_AT_PLUS_A', "
             "and 'COLAMD'. Reverting to default.",
             OptimizeWarning)
        permc_spec = 'MMD_AT_PLUS_A'

    # This can be an error
    if not sym_pos and cholesky:
        raise ValueError(
            "Invalid option combination 'sym_pos':False "
            "and 'cholesky':True: Cholesky decomposition is only possible "
            "for symmetric positive definite matrices.")

    cholesky = cholesky is None and sym_pos and not sparse and not lstsq

    iteration = 0
    complete = False    # will become True if solved in presolve
    undo = []

    # Convert lists to numpy arrays, etc...
    c, A_ub, b_ub, A_eq, b_eq, bounds = _clean_inputs(
        c, A_ub, b_ub, A_eq, b_eq, bounds)

    # Keep the original arrays to calculate slack/residuals for original
    # problem.
    c_o, A_ub_o, b_ub_o, A_eq_o, b_eq_o = c.copy(
    ), A_ub.copy(), b_ub.copy(), A_eq.copy(), b_eq.copy()

    # Solve trivial problem, eliminate variables, tighten bounds, etc...
    c0 = 0  # we might get a constant term in the objective
    if presolve is True:
        (c, c0, A_ub, b_ub, A_eq, b_eq, bounds, x, undo, complete, status,
            message) = _presolve(c, A_ub, b_ub, A_eq, b_eq, bounds, rr)

    # If not solved in presolve, solve it
    if not complete:
        # Convert problem to standard form
        A, b, c, c0 = _get_Abc(c, c0, A_ub, b_ub, A_eq, b_eq, bounds, undo)
        # Solve the problem
        x, status, message, iteration = _ip_hsd(A, b, c, c0, alpha0, beta,
                                                maxiter, disp, tol, sparse,
                                                lstsq, sym_pos, cholesky,
                                                pc, ip, permc_spec)

    # Eliminate artificial variables, re-introduce presolved variables, etc...
    # need modified bounds here to translate variables appropriately
    x, fun, slack, con, status, message = _postprocess(
        x, c_o, A_ub_o, b_ub_o, A_eq_o, b_eq_o,
        bounds, complete, undo, status, message)

    sol = {
        'x': x,
        'fun': fun,
        'slack': slack,
        'con': con,
        'status': status,
        'message': message,
        'nit': iteration,
        "success": status == 0}

    return OptimizeResult(sol)
