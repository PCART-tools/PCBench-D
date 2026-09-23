def linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None,
            bounds=None, method='simplex', callback=None,
            options=None):
    """
    Minimize a linear objective function subject to linear
    equality and inequality constraints.

    Linear Programming is intended to solve the following problem form::

        Minimize:     c^T * x

        Subject to:   A_ub * x <= b_ub
                      A_eq * x == b_eq

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
        1-D array of values representing the RHS of each equality constraint
        (row) in ``A_eq``.
    bounds : sequence, optional
        ``(min, max)`` pairs for each element in ``x``, defining
        the bounds on that parameter. Use None for one of ``min`` or
        ``max`` when there is no bound in that direction. By default
        bounds are ``(0, None)`` (non-negative)
        If a sequence containing a single tuple is provided, then ``min`` and
        ``max`` will be applied to all variables in the problem.
    method : str, optional
        Type of solver.  :ref:`'simplex' <optimize.linprog-simplex>`
        and :ref:`'interior-point' <optimize.linprog-interior-point>`
        are supported.
    callback : callable, optional (simplex only)
        If a callback function is provide, it will be called within each
        iteration of the simplex algorithm. The callback must have the
        signature ``callback(xk, **kwargs)`` where ``xk`` is the current
        solution vector and ``kwargs`` is a dictionary containing the
        following::

            "tableau" : The current Simplex algorithm tableau
            "nit" : The current iteration.
            "pivot" : The pivot (row, column) used for the next iteration.
            "phase" : Whether the algorithm is in Phase 1 or Phase 2.
            "basis" : The indices of the columns of the basic variables.

    options : dict, optional
        A dictionary of solver options. All methods accept the following
        generic options:

            maxiter : int
                Maximum number of iterations to perform.
            disp : bool
                Set to True to print convergence messages.

        For method-specific options, see :func:`show_options('linprog')`.

    Returns
    -------
    A `scipy.optimize.OptimizeResult` consisting of the following fields:

        x : ndarray
            The independent variable vector which optimizes the linear
            programming problem.
        fun : float
            Value of the objective function.
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

        nit : int
            The number of iterations performed.
        message : str
            A string descriptor of the exit status of the optimization.

    See Also
    --------
    show_options : Additional options accepted by the solvers

    Notes
    -----
    This section describes the available solvers that can be selected by the
    'method' parameter. The default method
    is :ref:`Simplex <optimize.linprog-simplex>`.
    :ref:`Interior point <optimize.linprog-interior-point>` is also available.

    Method *simplex* uses the simplex algorithm (as it relates to linear
    programming, NOT the Nelder-Mead simplex) [1]_, [2]_. This algorithm
    should be reasonably reliable and fast for small problems.

    .. versionadded:: 0.15.0

    Method *interior-point* uses the primal-dual path following algorithm
    as outlined in [4]_. This algorithm is intended to provide a faster
    and more reliable alternative to *simplex*, especially for large,
    sparse problems. Note, however, that the solution returned may be slightly
    less accurate than that of the simplex method and may not correspond with a
    vertex of the polytope defined by the constraints.

    References
    ----------
    .. [1] Dantzig, George B., Linear programming and extensions. Rand
           Corporation Research Study Princeton Univ. Press, Princeton, NJ,
           1963
    .. [2] Hillier, S.H. and Lieberman, G.J. (1995), "Introduction to
           Mathematical Programming", McGraw-Hill, Chapter 4.
    .. [3] Bland, Robert G. New finite pivoting rules for the simplex method.
           Mathematics of Operations Research (2), 1977: pp. 103-107.
    .. [4] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.
    .. [5] Andersen, Erling D. "Finding all linearly dependent rows in
           large-scale linear programming." Optimization Methods and Software
           6.3 (1995): 219-227.
    .. [6] Freund, Robert M. "Primal-Dual Interior-Point Methods for Linear
           Programming based on Newton's Method." Unpublished Course Notes,
           March 2004. Available 2/25/2017 at
           https://ocw.mit.edu/courses/sloan-school-of-management/15-084j-nonlinear-programming-spring-2004/lecture-notes/lec14_int_pt_mthd.pdf
    .. [7] Fourer, Robert. "Solving Linear Programs by Interior-Point Methods."
           Unpublished Course Notes, August 26, 2005. Available 2/25/2017 at
           http://www.4er.org/CourseNotes/Book%20B/B-III.pdf
    .. [8] Andersen, Erling D., and Knud D. Andersen. "Presolving in linear
           programming." Mathematical Programming 71.2 (1995): 221-245.
    .. [9] Bertsimas, Dimitris, and J. Tsitsiklis. "Introduction to linear
           programming." Athena Scientific 1 (1997): 997.
    .. [10] Andersen, Erling D., et al. Implementation of interior point
            methods for large scale linear programming. HEC/Universite de
            Geneve, 1996.

    Examples
    --------
    Consider the following problem:

    Minimize: f = -1*x[0] + 4*x[1]

    Subject to: -3*x[0] + 1*x[1] <= 6
                 1*x[0] + 2*x[1] <= 4
                            x[1] >= -3

    where:  -inf <= x[0] <= inf

    This problem deviates from the standard linear programming problem.
    In standard form, linear programming problems assume the variables x are
    non-negative.  Since the variables don't have standard bounds where
    0 <= x <= inf, the bounds of the variables must be explicitly set.

    There are two upper-bound constraints, which can be expressed as

    dot(A_ub, x) <= b_ub

    The input for this problem is as follows:

    >>> c = [-1, 4]
    >>> A = [[-3, 1], [1, 2]]
    >>> b = [6, 4]
    >>> x0_bounds = (None, None)
    >>> x1_bounds = (-3, None)
    >>> from scipy.optimize import linprog
    >>> res = linprog(c, A_ub=A, b_ub=b, bounds=(x0_bounds, x1_bounds),
    ...               options={"disp": True})
    Optimization terminated successfully.
         Current function value: -22.000000
         Iterations: 1
    >>> print(res)
         fun: -22.0
     message: 'Optimization terminated successfully.'
         nit: 1
       slack: array([ 39.,   0.])
      status: 0
     success: True
           x: array([ 10.,  -3.])

    Note the actual objective value is 11.428571.  In this case we minimized
    the negative of the objective function.

    """
    meth = method.lower()
    if options is None:
        options = {}

    if meth == 'simplex':
        return _linprog_simplex(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                                bounds=bounds, callback=callback, **options)
    elif meth == 'interior-point':
        return _linprog_ip(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                           bounds=bounds, callback=callback, **options)
    else:
        raise ValueError('Unknown solver %s' % method)
