def _pivot_row(T, pivcol, phase, tol=1.0E-12):
    """
    Given a linear programming simplex tableau, determine the row for the
    pivot operation.

    Parameters
    ----------
    T : 2D ndarray
        The simplex tableau.
    pivcol : int
        The index of the pivot column.
    phase : int
        The phase of the simplex algorithm (1 or 2).
    tol : float
        Elements in the pivot column smaller than tol will not be considered
        for pivoting.  Nominally this value is zero, but numerical issues
        cause a tolerance about zero to be necessary.

    Returns
    -------
    status: bool
        True if a suitable pivot row was found, otherwise False.  A return
        of False indicates that the linear programming problem is unbounded.
    row: int
        The index of the row of the pivot element.  If status is False, row
        will be returned as nan.
    """
    if phase == 1:
        k = 2
    else:
        k = 1
    ma = np.ma.masked_where(T[:-k, pivcol] <= tol, T[:-k, pivcol], copy=False)
    if ma.count() == 0:
        return False, np.nan
    mb = np.ma.masked_where(T[:-k, pivcol] <= tol, T[:-k, -1], copy=False)
    q = mb / ma
    return True, np.ma.where(q == q.min())[0][0]
