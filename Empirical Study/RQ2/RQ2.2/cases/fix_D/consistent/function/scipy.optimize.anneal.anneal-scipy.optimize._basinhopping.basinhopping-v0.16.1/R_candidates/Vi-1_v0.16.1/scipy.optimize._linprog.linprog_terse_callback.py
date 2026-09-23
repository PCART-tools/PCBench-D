def linprog_terse_callback(xk, **kwargs):
    """
    A sample callback function demonstrating the linprog callback interface.
    This callback produces brief output to sys.stdout before each iteration
    and after the final iteration of the simplex algorithm.

    Parameters
    ----------
    xk : array_like
        The current solution vector.
    **kwargs : dict
        A dictionary containing the following parameters:

        tableau : array_like
            The current tableau of the simplex algorithm.
            Its structure is defined in _solve_simplex.
        vars : tuple(str, ...)
            Column headers for each column in tableau.
            "x[i]" for actual variables, "s[i]" for slack surplus variables,
            "a[i]" for artificial variables, and "RHS" for the constraint
            RHS vector.
        phase : int
            The current Phase of the simplex algorithm (1 or 2)
        nit : int
            The current iteration number.
        pivot : tuple(int, int)
            The index of the tableau selected as the next pivot,
            or nan if no pivot exists
        basics : list[tuple(int, float)]
            A list of the current basic variables.
            Each element contains the index of a basic variable and
            its value.
        complete : bool
            True if the simplex algorithm has completed
            (and this is the final call to callback), otherwise False.
    """
    nit = kwargs["nit"]

    if nit == 0:
        print("Iter:   X:")
    print("{: <5d}   ".format(nit), end="")
    print(xk)
