def _pivot_col(T, tol=1.0E-12, bland=False):
    """
    Given a linear programming simplex tableau, determine the column
    of the variable to enter the basis.

    Parameters
    ----------
    T : 2D ndarray
        The simplex tableau.
    tol : float
        Elements in the objective row larger than -tol will not be considered
        for pivoting.  Nominally this value is zero, but numerical issues
        cause a tolerance about zero to be necessary.
    bland : bool
        If True, use Bland's rule for selection of the column (select the
        first column with a negative coefficient in the objective row,
        regardless of magnitude).

    Returns
    -------
    status: bool
        True if a suitable pivot column was found, otherwise False.
        A return of False indicates that the linear programming simplex
        algorithm is complete.
    col: int
        The index of the column of the pivot element.
        If status is False, col will be returned as nan.
    """
    ma = np.ma.masked_where(T[-1, :-1] >= -tol, T[-1, :-1], copy=False)
    if ma.count() == 0:
        return False, np.nan
    if bland:
        return True, np.where(ma.mask == False)[0][0]
    return True, np.ma.where(ma == ma.min())[0][0]
