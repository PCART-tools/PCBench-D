def _linprog_simplex(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None,
            bounds=None, maxiter=1000, disp=False, callback=None,
            tol=1.0E-12, bland=False, **unknown_options):
    """
    Solve the following linear programming problem via a two-phase
    simplex algorithm.

    minimize:     c^T * x

    subject to:   A_ub * x <= b_ub
                  A_eq * x == b_eq

    Parameters
    ----------
    c : array_like
        Coefficients of the linear objective function to be minimized.
    A_ub : array_like
        2-D array which, when matrix-multiplied by x, gives the values of the
        upper-bound inequality constraints at x.
    b_ub : array_like
        1-D array of values representing the upper-bound of each inequality
        constraint (row) in A_ub.
    A_eq : array_like
        2-D array which, when matrix-multiplied by x, gives the values of the
        equality constraints at x.
    b_eq : array_like
        1-D array of values representing the RHS of each equality constraint
        (row) in A_eq.
    bounds : array_like
        The bounds for each independent variable in the solution, which can take
        one of three forms::
        None : The default bounds, all variables are non-negative.
        (lb, ub) : If a 2-element sequence is provided, the same
                  lower bound (lb) and upper bound (ub) will be applied
                  to all variables.
        [(lb_0, ub_0), (lb_1, ub_1), ...] : If an n x 2 sequence is provided,
                  each variable x_i will be bounded by lb[i] and ub[i].
        Infinite bounds are specified using -np.inf (negative)
        or np.inf (positive).
    callback : callable
        If a callback function is provide, it will be called within each
        iteration of the simplex algorithm. The callback must have the
        signature `callback(xk, **kwargs)` where xk is the current solution
        vector and kwargs is a dictionary containing the following::
        "tableau" : The current Simplex algorithm tableau
        "nit" : The current iteration.
        "pivot" : The pivot (row, column) used for the next iteration.
        "phase" : Whether the algorithm is in Phase 1 or Phase 2.
        "bv" : A structured array containing a string representation of each
               basic variable and its current value.

    Options
    -------
    maxiter : int
       The maximum number of iterations to perform.
    disp : bool
        If True, print exit status message to sys.stdout
    tol : float
        The tolerance which determines when a solution is "close enough" to zero
        in Phase 1 to be considered a basic feasible solution or close enough
        to positive to to serve as an optimal solution.
    bland : bool
        If True, use Bland's anti-cycling rule [3] to choose pivots to
        prevent cycling.  If False, choose pivots which should lead to a
        converged solution more quickly.  The latter method is subject to
        cycling (non-convergence) in rare instances.

    Returns
    -------
    A scipy.optimize.OptimizeResult consisting of the following fields::
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

    Examples
    --------
    Consider the following problem:

    Minimize: f = -1*x[0] + 4*x[1]

    Subject to: -3*x[0] + 1*x[1] <= 6
                 1*x[0] + 2*x[1] <= 4
                            x[1] >= -3

    where:  -inf <= x[0] <= inf

    This problem deviates from the standard linear programming problem.  In
    standard form, linear programming problems assume the variables x are
    non-negative.  Since the variables don't have standard bounds where
    0 <= x <= inf, the bounds of the variables must be explicitly set.

    There are two upper-bound constraints, which can be expressed as

    dot(A_ub, x) <= b_ub

    The input for this problem is as follows:

    >>> from scipy.optimize import linprog
    >>> c = [-1, 4]
    >>> A = [[-3, 1], [1, 2]]
    >>> b = [6, 4]
    >>> x0_bnds = (None, None)
    >>> x1_bnds = (-3, None)
    >>> res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds))
    >>> print(res)
         fun: -22.0
     message: 'Optimization terminated successfully.'
         nit: 1
       slack: array([ 39.,   0.])
      status: 0
     success: True
           x: array([ 10.,  -3.])

    References
    ----------
    .. [1] Dantzig, George B., Linear programming and extensions. Rand
           Corporation Research Study Princeton Univ. Press, Princeton, NJ, 1963
    .. [2] Hillier, S.H. and Lieberman, G.J. (1995), "Introduction to
           Mathematical Programming", McGraw-Hill, Chapter 4.
    .. [3] Bland, Robert G. New finite pivoting rules for the simplex method.
           Mathematics of Operations Research (2), 1977: pp. 103-107.
    """
    _check_unknown_options(unknown_options)

    status = 0
    messages = {0: "Optimization terminated successfully.",
                1: "Iteration limit reached.",
                2: "Optimization failed. Unable to find a feasible"
                   " starting point.",
                3: "Optimization failed. The problem appears to be unbounded.",
                4: "Optimization failed. Singular matrix encountered."}
    have_floor_variable = False

    cc = np.asarray(c)

    # The initial value of the objective function element in the tableau
    f0 = 0

    # The number of variables as given by c
    n = len(c)

    # Convert the input arguments to arrays (sized to zero if not provided)
    Aeq = np.asarray(A_eq) if A_eq is not None else np.empty([0, len(cc)])
    Aub = np.asarray(A_ub) if A_ub is not None else np.empty([0, len(cc)])
    beq = np.ravel(np.asarray(b_eq)) if b_eq is not None else np.empty([0])
    bub = np.ravel(np.asarray(b_ub)) if b_ub is not None else np.empty([0])

    # Analyze the bounds and determine what modifications to be made to
    # the constraints in order to accommodate them.
    L = np.zeros(n, dtype=np.float64)
    U = np.ones(n, dtype=np.float64)*np.inf
    if bounds is None or len(bounds) == 0:
        pass
    elif len(bounds) == 2 and not hasattr(bounds[0], '__len__'):
        # All bounds are the same
        a = bounds[0] if bounds[0] is not None else -np.inf
        b = bounds[1] if bounds[1] is not None else np.inf
        L = np.asarray(n*[a], dtype=np.float64)
        U = np.asarray(n*[b], dtype=np.float64)
    else:
        if len(bounds) != n:
            status = -1
            message = ("Invalid input for linprog with method = 'simplex'.  "
                      "Length of bounds is inconsistent with the length of c")
        else:
            try:
                for i in range(n):
                    if len(bounds[i]) != 2:
                        raise IndexError()
                    L[i] = bounds[i][0] if bounds[i][0] is not None else -np.inf
                    U[i] = bounds[i][1] if bounds[i][1] is not None else np.inf
            except IndexError:
                status = -1
                message = ("Invalid input for linprog with "
                           "method = 'simplex'.  bounds must be a n x 2 "
                           "sequence/array where n = len(c).")

    if np.any(L == -np.inf):
        # If any lower-bound constraint is a free variable
        # add the first column variable as the "floor" variable which
        # accommodates the most negative variable in the problem.
        n = n + 1
        L = np.concatenate([np.array([0]), L])
        U = np.concatenate([np.array([np.inf]), U])
        cc = np.concatenate([np.array([0]), cc])
        Aeq = np.hstack([np.zeros([Aeq.shape[0], 1]), Aeq])
        Aub = np.hstack([np.zeros([Aub.shape[0], 1]), Aub])
        have_floor_variable = True

    # Now before we deal with any variables with lower bounds < 0,
    # deal with finite bounds which can be simply added as new constraints.
    # Also validate bounds inputs here.
    for i in range(n):
        if(L[i] > U[i]):
            status = -1
            message = ("Invalid input for linprog with method = 'simplex'.  "
                       "Lower bound %d is greater than upper bound %d" % (i, i))

        if np.isinf(L[i]) and L[i] > 0:
            status = -1
            message = ("Invalid input for linprog with method = 'simplex'.  "
                       "Lower bound may not be +infinity")

        if np.isinf(U[i]) and U[i] < 0:
            status = -1
            message = ("Invalid input for linprog with method = 'simplex'.  "
                       "Upper bound may not be -infinity")

        if np.isfinite(L[i]) and L[i] > 0:
            # Add a new lower-bound (negative upper-bound) constraint
            Aub = np.vstack([Aub, np.zeros(n)])
            Aub[-1, i] = -1
            bub = np.concatenate([bub, np.array([-L[i]])])
            L[i] = 0

        if np.isfinite(U[i]):
            # Add a new upper-bound constraint
            Aub = np.vstack([Aub, np.zeros(n)])
            Aub[-1, i] = 1
            bub = np.concatenate([bub, np.array([U[i]])])
            U[i] = np.inf

    # Now find negative lower bounds (finite or infinite) which require a
    # change of variables or free variables and handle them appropriately
    for i in range(0, n):
        if L[i] < 0:
            if np.isfinite(L[i]) and L[i] < 0:
                # Add a change of variables for x[i]
                # For each row in the constraint matrices, we take the
                # coefficient from column i in A,
                # and subtract the product of that and L[i] to the RHS b
                beq = beq - Aeq[:, i] * L[i]
                bub = bub - Aub[:, i] * L[i]
                # We now have a nonzero initial value for the objective
                # function as well.
                f0 = f0 - cc[i] * L[i]
            else:
                # This is an unrestricted variable, let x[i] = u[i] - v[0]
                # where v is the first column in all matrices.
                Aeq[:, 0] = Aeq[:, 0] - Aeq[:, i]
                Aub[:, 0] = Aub[:, 0] - Aub[:, i]
                cc[0] = cc[0] - cc[i]

        if np.isinf(U[i]):
            if U[i] < 0:
                status = -1
                message = ("Invalid input for linprog with "
                           "method = 'simplex'.  Upper bound may not be -inf.")

    # The number of upper bound constraints (rows in A_ub and elements in b_ub)
    mub = len(bub)

    # The number of equality constraints (rows in A_eq and elements in b_eq)
    meq = len(beq)

    # The total number of constraints
    m = mub+meq

    # The number of slack variables (one for each of the upper-bound constraints)
    n_slack = mub

    # The number of artificial variables (one for each lower-bound and equality
    # constraint)
    n_artificial = meq + np.count_nonzero(bub < 0)

    try:
        Aub_rows, Aub_cols = Aub.shape
    except ValueError:
        raise ValueError("Invalid input.  A_ub must be two-dimensional")

    try:
        Aeq_rows, Aeq_cols = Aeq.shape
    except ValueError:
        raise ValueError("Invalid input.  A_eq must be two-dimensional")

    if Aeq_rows != meq:
        status = -1
        message = ("Invalid input for linprog with method = 'simplex'.  "
                   "The number of rows in A_eq must be equal "
                   "to the number of values in b_eq")

    if Aub_rows != mub:
        status = -1
        message = ("Invalid input for linprog with method = 'simplex'.  "
                   "The number of rows in A_ub must be equal "
                   "to the number of values in b_ub")

    if Aeq_cols > 0 and Aeq_cols != n:
        status = -1
        message = ("Invalid input for linprog with method = 'simplex'.  "
                   "Number of columns in A_eq must be equal "
                   "to the size of c")

    if Aub_cols > 0 and Aub_cols != n:
        status = -1
        message = ("Invalid input for linprog with method = 'simplex'.  "
                   "Number of columns in A_ub must be equal to the size of c")

    if status != 0:
        # Invalid inputs provided
        raise ValueError(message)

    # Create the tableau
    T = np.zeros([m+2, n+n_slack+n_artificial+1])

    # Insert objective into tableau
    T[-2, :n] = cc
    T[-2, -1] = f0

    b = T[:-2, -1]

    if meq > 0:
        # Add Aeq to the tableau
        T[:meq, :n] = Aeq
        # Add beq to the tableau
        b[:meq] = beq
    if mub > 0:
        # Add Aub to the tableau
        T[meq:meq+mub, :n] = Aub
        # At bub to the tableau
        b[meq:meq+mub] = bub
        # Add the slack variables to the tableau
        np.fill_diagonal(T[meq:m, n:n+n_slack], 1)

    # Further set up the tableau.
    # If a row corresponds to an equality constraint or a negative b (a lower
    # bound constraint), then an artificial variable is added for that row.
    # Also, if b is negative, first flip the signs in that constraint.
    slcount = 0
    avcount = 0
    basis = np.zeros(m, dtype=int)
    r_artificial = np.zeros(n_artificial, dtype=int)
    for i in range(m):
        if i < meq or b[i] < 0:
            # basic variable i is in column n+n_slack+avcount
            basis[i] = n+n_slack+avcount
            r_artificial[avcount] = i
            avcount += 1
            if b[i] < 0:
                b[i] *= -1
                T[i, :-1] *= -1
            T[i, basis[i]] = 1
            T[-1, basis[i]] = 1
        else:
            # basic variable i is in column n+slcount
            basis[i] = n+slcount
            slcount += 1

    # Make the artificial variables basic feasible variables by subtracting
    # each row with an artificial variable from the Phase 1 objective
    for r in r_artificial:
        T[-1, :] = T[-1, :] - T[r, :]

    nit1, status = _solve_simplex(T, n, basis, phase=1, callback=callback,
                                  maxiter=maxiter, tol=tol, bland=bland)

    # if pseudo objective is zero, remove the last row from the tableau and
    # proceed to phase 2
    if abs(T[-1, -1]) < tol:
        # Remove the pseudo-objective row from the tableau
        T = T[:-1, :]
        # Remove the artificial variable columns from the tableau
        T = np.delete(T, np.s_[n+n_slack:n+n_slack+n_artificial], 1)
    else:
        # Failure to find a feasible starting point
        status = 2

    if status != 0:
        message = messages[status]
        if disp:
            print(message)
        return OptimizeResult(x=np.nan, fun=-T[-1, -1], nit=nit1, status=status,
                      message=message, success=False)

    # Phase 2
    nit2, status = _solve_simplex(T, n, basis, maxiter=maxiter-nit1, phase=2,
                                  callback=callback, tol=tol, nit0=nit1,
                                  bland=bland)

    solution = np.zeros(n+n_slack+n_artificial)
    solution[basis[:m]] = T[:m, -1]
    x = solution[:n]
    slack = solution[n:n+n_slack]

    # For those variables with finite negative lower bounds,
    # reverse the change of variables
    masked_L = np.ma.array(L, mask=np.isinf(L), fill_value=0.0).filled()
    x = x + masked_L

    # For those variables with infinite negative lower bounds,
    # take x[i] as the difference between x[i] and the floor variable.
    if have_floor_variable:
        for i in range(1, n):
            if np.isinf(L[i]):
                x[i] -= x[0]
        x = x[1:]

    # Optimization complete at this point
    obj = -T[-1, -1]

    if status in (0, 1):
        if disp:
            print(messages[status])
            print("         Current function value: {0: <12.6f}".format(obj))
            print("         Iterations: {0:d}".format(nit2))
    else:
        if disp:
            print(messages[status])
            print("         Iterations: {0:d}".format(nit2))

    return OptimizeResult(x=x, fun=obj, nit=int(nit2), status=status, slack=slack,
                  message=messages[status], success=(status == 0))
