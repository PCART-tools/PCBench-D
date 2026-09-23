def _clean_inputs(
        c,
        A_ub=None,
        b_ub=None,
        A_eq=None,
        b_eq=None,
        bounds=None):
    """
    Given user inputs for a linear programming problem, return the
    objective vector, upper bound constraints, equality constraints,
    and simple bounds in a preferred format.

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

    Returns
    -------
    c : 1-D array
        Coefficients of the linear objective function to be minimized.
    A_ub : 2-D array
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the upper-bound inequality constraints at ``x``.
    b_ub : 1-D array
        1-D array of values representing the upper-bound of each inequality
        constraint (row) in ``A_ub``.
    A_eq : 2-D array
        2-D array which, when matrix-multiplied by ``x``, gives the values of
        the equality constraints at ``x``.
    b_eq : 1-D array
        1-D array of values representing the RHS of each equality constraint
        (row) in ``A_eq``.
    bounds : sequence of tuples
        ``(min, max)`` pairs for each element in ``x``, defining
        the bounds on that parameter. Use None for each of ``min`` or
        ``max`` when there is no bound in that direction. By default
        bounds are ``(0, None)`` (non-negative)

    """

    try:
        if c is None:
            raise TypeError
        try:
            c = np.asarray(c, dtype=float).copy().squeeze()
        except BaseException:  # typically a ValueError and shouldn't be, IMO
            raise TypeError
        if c.size == 1:
            c = c.reshape((-1))
        n_x = len(c)
        if n_x == 0 or len(c.shape) != 1:
            raise ValueError(
                "Invalid input for linprog: c should be a 1D array; it must "
                "not have more than one non-singleton dimension")
        if not(np.isfinite(c).all()):
            raise ValueError(
                "Invalid input for linprog: c must not contain values "
                "inf, nan, or None")
    except TypeError:
        raise TypeError(
            "Invalid input for linprog: c must be a 1D array of numerical "
            "coefficients")

    try:
        try:
            if sps.issparse(A_eq) or sps.issparse(A_ub):
                A_ub = sps.coo_matrix(
                    (0, n_x), dtype=float) if A_ub is None else sps.coo_matrix(
                    A_ub, dtype=float).copy()
            else:
                A_ub = np.zeros(
                    (0, n_x), dtype=float) if A_ub is None else np.asarray(
                    A_ub, dtype=float).copy()
        except BaseException:
            raise TypeError
        n_ub = A_ub.shape[0]
        if len(A_ub.shape) != 2 or A_ub.shape[1] != len(c):
            raise ValueError(
                "Invalid input for linprog: A_ub must have exactly two "
                "dimensions, and the number of columns in A_ub must be "
                "equal to the size of c ")
        if (sps.issparse(A_ub) and not np.isfinite(A_ub.data).all()
                or not sps.issparse(A_ub) and not np.isfinite(A_ub).all()):
            raise ValueError(
                "Invalid input for linprog: A_ub must not contain values "
                "inf, nan, or None")
    except TypeError:
        raise TypeError(
            "Invalid input for linprog: A_ub must be a numerical 2D array "
            "with each row representing an upper bound inequality constraint")

    try:
        try:
            b_ub = np.array(
                [], dtype=float) if b_ub is None else np.asarray(
                b_ub, dtype=float).copy().squeeze()
        except BaseException:
            raise TypeError
        if b_ub.size == 1:
            b_ub = b_ub.reshape((-1))
        if len(b_ub.shape) != 1:
            raise ValueError(
                "Invalid input for linprog: b_ub should be a 1D array; it "
                "must not have more than one non-singleton dimension")
        if len(b_ub) != n_ub:
            raise ValueError(
                "Invalid input for linprog: The number of rows in A_ub must "
                "be equal to the number of values in b_ub")
        if not(np.isfinite(b_ub).all()):
            raise ValueError(
                "Invalid input for linprog: b_ub must not contain values "
                "inf, nan, or None")
    except TypeError:
        raise TypeError(
            "Invalid input for linprog: b_ub must be a 1D array of "
            "numerical values, each representing the upper bound of an "
            "inequality constraint (row) in A_ub")

    try:
        try:
            if sps.issparse(A_eq) or sps.issparse(A_ub):
                A_eq = sps.coo_matrix(
                    (0, n_x), dtype=float) if A_eq is None else sps.coo_matrix(
                    A_eq, dtype=float).copy()
            else:
                A_eq = np.zeros(
                    (0, n_x), dtype=float) if A_eq is None else np.asarray(
                    A_eq, dtype=float).copy()
        except BaseException:
            raise TypeError
        n_eq = A_eq.shape[0]
        if len(A_eq.shape) != 2 or A_eq.shape[1] != len(c):
            raise ValueError(
                "Invalid input for linprog: A_eq must have exactly two "
                "dimensions, and the number of columns in A_eq must be "
                "equal to the size of c ")

        if (sps.issparse(A_eq) and not np.isfinite(A_eq.data).all()
                or not sps.issparse(A_eq) and not np.isfinite(A_eq).all()):
            raise ValueError(
                "Invalid input for linprog: A_eq must not contain values "
                "inf, nan, or None")
    except TypeError:
        raise TypeError(
            "Invalid input for linprog: A_eq must be a 2D array with each "
            "row representing an equality constraint")

    try:
        try:
            b_eq = np.array(
                [], dtype=float) if b_eq is None else np.asarray(
                b_eq, dtype=float).copy().squeeze()
        except BaseException:
            raise TypeError
        if b_eq.size == 1:
            b_eq = b_eq.reshape((-1))
        if len(b_eq.shape) != 1:
            raise ValueError(
                "Invalid input for linprog: b_eq should be a 1D array; it "
                "must not have more than one non-singleton dimension")
        if len(b_eq) != n_eq:
            raise ValueError(
                "Invalid input for linprog: the number of rows in A_eq "
                "must be equal to the number of values in b_eq")
        if not(np.isfinite(b_eq).all()):
            raise ValueError(
                "Invalid input for linprog: b_eq must not contain values "
                "inf, nan, or None")
    except TypeError:
        raise TypeError(
            "Invalid input for linprog: b_eq must be a 1D array of "
            "numerical values, each representing the right hand side of an "
            "equality constraints (row) in A_eq")

    # "If a sequence containing a single tuple is provided, then min and max
    # will be applied to all variables in the problem."
    # linprog doesn't treat this right: it didn't accept a list with one tuple
    # in it
    try:
        if isinstance(bounds, str):
            raise TypeError
        if bounds is None or len(bounds) == 0:
            bounds = [(0, None)] * n_x
        elif len(bounds) == 1:
            b = bounds[0]
            if len(b) != 2:
                raise ValueError(
                    "Invalid input for linprog: exactly one lower bound and "
                    "one upper bound must be specified for each element of x")
            bounds = [b] * n_x
        elif len(bounds) == n_x:
            try:
                len(bounds[0])
            except BaseException:
                bounds = [(bounds[0], bounds[1])] * n_x
            for i, b in enumerate(bounds):
                if len(b) != 2:
                    raise ValueError(
                        "Invalid input for linprog, bound " +
                        str(i) +
                        " " +
                        str(b) +
                        ": exactly one lower bound and one upper bound must "
                        "be specified for each element of x")
        elif (len(bounds) == 2 and np.isreal(bounds[0])
                and np.isreal(bounds[1])):
            bounds = [(bounds[0], bounds[1])] * n_x
        else:
            raise ValueError(
                "Invalid input for linprog: exactly one lower bound and one "
                "upper bound must be specified for each element of x")

        clean_bounds = []  # also creates a copy so user's object isn't changed
        for i, b in enumerate(bounds):
            if b[0] is not None and b[1] is not None and b[0] > b[1]:
                raise ValueError(
                    "Invalid input for linprog, bound " +
                    str(i) +
                    " " +
                    str(b) +
                    ": a lower bound must be less than or equal to the "
                    "corresponding upper bound")
            if b[0] == np.inf:
                raise ValueError(
                    "Invalid input for linprog, bound " +
                    str(i) +
                    " " +
                    str(b) +
                    ": infinity is not a valid lower bound")
            if b[1] == -np.inf:
                raise ValueError(
                    "Invalid input for linprog, bound " +
                    str(i) +
                    " " +
                    str(b) +
                    ": negative infinity is not a valid upper bound")
            lb = float(b[0]) if b[0] is not None and b[0] != -np.inf else None
            ub = float(b[1]) if b[1] is not None and b[1] != np.inf else None
            clean_bounds.append((lb, ub))
        bounds = clean_bounds
    except ValueError as e:
        if "could not convert string to float" in e.args[0]:
            raise TypeError
        else:
            raise e
    except TypeError as e:
        print(e)
        raise TypeError(
            "Invalid input for linprog: bounds must be a sequence of "
            "(min,max) pairs, each defining bounds on an element of x ")

    return c, A_ub, b_ub, A_eq, b_eq, bounds
