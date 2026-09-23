def solve_lyapunov(a, q):
    """
    Solves the continuous Lyapunov equation :math:`AX + XA^H = Q`.

    Uses the Bartels-Stewart algorithm to find :math:`X`.

    Parameters
    ----------
    a : array_like
        A square matrix

    q : array_like
        Right-hand side square matrix

    Returns
    -------
    x : array_like
        Solution to the continuous Lyapunov equation

    See Also
    --------
    solve_sylvester : computes the solution to the Sylvester equation

    Notes
    -----
    Because the continuous Lyapunov equation is just a special form of the
    Sylvester equation, this solver relies entirely on solve_sylvester for a
    solution.

    .. versionadded:: 0.11.0

    """

    return solve_sylvester(a, a.conj().transpose(), q)
