def _get_solver(sparse=False, lstsq=False, sym_pos=True, cholesky=True):
    """
    Given solver options, return a handle to the appropriate linear system
    solver.

    Parameters
    ----------
    sparse : bool
        True if the system to be solved is sparse. This is typically set
        True when the original ``A_ub`` and ``A_eq`` arrays are sparse.
    lstsq : bool
        True if the system is ill-conditioned and/or (nearly) singular and
        thus a more robust least-squares solver is desired. This is sometimes
        needed as the solution is approached.
    sym_pos : bool
        True if the system matrix is symmetric positive definite
        Sometimes this needs to be set false as the solution is approached,
        even when the system should be symmetric positive definite, due to
        numerical difficulties.
    cholesky : bool
        True if the system is to be solved by Cholesky, rather than LU,
        decomposition. This is typically faster unless the problem is very
        small or prone to numerical difficulties.

    Returns
    -------
    solve : function
        Handle to the appropriate solver function

    """
    if sparse:
        if lstsq or not(sym_pos):
            def solve(M, r, sym_pos=False):
                return sps.linalg.lsqr(M, r)[0]
        else:
            # this is not currently used; it is replaced by splu solve
            # TODO: expose use of this as an option
            def solve(M, r):
                return sps.linalg.spsolve(M, r, permc_spec="MMD_AT_PLUS_A")

    else:
        if lstsq:  # sometimes necessary as solution is approached
            def solve(M, r):
                return sp.linalg.lstsq(M, r)[0]
        elif cholesky:
            solve = sp.linalg.cho_solve
        else:
            # this seems to cache the matrix factorization, so solving
            # with multiple right hand sides is much faster
            def solve(M, r, sym_pos=sym_pos):
                return sp.linalg.solve(M, r, sym_pos=sym_pos)

    return solve
