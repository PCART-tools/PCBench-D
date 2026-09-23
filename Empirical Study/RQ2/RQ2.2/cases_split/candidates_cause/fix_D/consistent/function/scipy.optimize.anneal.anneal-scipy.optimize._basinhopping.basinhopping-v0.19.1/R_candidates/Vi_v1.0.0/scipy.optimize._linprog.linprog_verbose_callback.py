def linprog_verbose_callback(xk, **kwargs):
    """
    A sample callback function demonstrating the linprog callback interface.
    This callback produces detailed output to sys.stdout before each iteration
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
        phase : int
            The current Phase of the simplex algorithm (1 or 2)
        nit : int
            The current iteration number.
        pivot : tuple(int, int)
            The index of the tableau selected as the next pivot,
            or nan if no pivot exists
        basis : array(int)
            A list of the current basic variables.
            Each element contains the name of a basic variable and its value.
        complete : bool
            True if the simplex algorithm has completed
            (and this is the final call to callback), otherwise False.
    """
    tableau = kwargs["tableau"]
    nit = kwargs["nit"]
    pivrow, pivcol = kwargs["pivot"]
    phase = kwargs["phase"]
    basis = kwargs["basis"]
    complete = kwargs["complete"]

    saved_printoptions = np.get_printoptions()
    np.set_printoptions(linewidth=500,
                        formatter={'float': lambda x: "{0: 12.4f}".format(x)})
    if complete:
        print("--------- Iteration Complete - Phase {0:d} -------\n".format(phase))
        print("Tableau:")
    elif nit == 0:
        print("--------- Initial Tableau - Phase {0:d} ----------\n".format(phase))

    else:
        print("--------- Iteration {0:d}  - Phase {1:d} --------\n".format(nit, phase))
        print("Tableau:")

    if nit >= 0:
        print("" + str(tableau) + "\n")
        if not complete:
            print("Pivot Element: T[{0:.0f}, {1:.0f}]\n".format(pivrow, pivcol))
        print("Basic Variables:", basis)
        print()
        print("Current Solution:")
        print("x = ", xk)
        print()
        print("Current Objective Value:")
        print("f = ", -tableau[-1, -1])
        print()
    np.set_printoptions(**saved_printoptions)
